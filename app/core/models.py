"""
Core models for the EcoGenomics Suite.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Project(models.Model):
    """
    Research project model.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='collaborated_projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_project'
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.name


class DataFile(models.Model):
    """
    Uploaded data files.
    """
    FILE_TYPE_CHOICES = [
        ('genomic', 'Genomic Data'),
        ('environmental', 'Environmental Data'),
        ('metadata', 'Metadata'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='data_files')
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='data_files/%Y/%m/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'core_datafile'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.name} ({self.project.name})"


class AnalysisJob(models.Model):
    """
    Analysis job tracking.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    ANALYSIS_TYPE_CHOICES = [
        ('diversity', 'Diversity Analysis'),
        ('composition', 'Taxonomic Composition'),
        ('differential', 'Differential Analysis'),
        ('correlation', 'Environmental Correlation'),
        ('phylogenetic', 'Phylogenetic Analysis'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='analysis_jobs')
    name = models.CharField(max_length=200)
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPE_CHOICES)
    input_files = models.ManyToManyField(DataFile, related_name='analysis_jobs')
    parameters = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0)  # 0-100
    error_message = models.TextField(blank=True)
    started_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'core_analysisjob'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    @property
    def duration(self):
        if self.completed_at:
            return self.completed_at - self.started_at
        return timezone.now() - self.started_at