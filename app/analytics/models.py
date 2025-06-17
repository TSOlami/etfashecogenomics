"""
Analytics models for storing analysis results.
"""
from django.db import models
from django.conf import settings
from core.models import AnalysisJob
import uuid


class AnalysisResult(models.Model):
    """
    Store analysis results and visualizations.
    """
    RESULT_TYPE_CHOICES = [
        ('chart', 'Chart Data'),
        ('table', 'Table Data'),
        ('heatmap', 'Heatmap Data'),
        ('tree', 'Phylogenetic Tree'),
        ('network', 'Network Data'),
        ('summary', 'Summary Statistics'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(AnalysisJob, on_delete=models.CASCADE, related_name='results')
    name = models.CharField(max_length=200)
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE_CHOICES)
    data = models.JSONField()  # Store the actual result data
    metadata = models.JSONField(default=dict)  # Additional metadata
    file_path = models.CharField(max_length=500, blank=True)  # Path to result files
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_analysisresult'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.job.name})"


class Visualization(models.Model):
    """
    Store visualization configurations and data.
    """
    CHART_TYPE_CHOICES = [
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('scatter', 'Scatter Plot'),
        ('heatmap', 'Heatmap'),
        ('pie', 'Pie Chart'),
        ('box', 'Box Plot'),
        ('violin', 'Violin Plot'),
        ('network', 'Network Graph'),
        ('tree', 'Tree Diagram'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    result = models.ForeignKey(AnalysisResult, on_delete=models.CASCADE, related_name='visualizations')
    title = models.CharField(max_length=200)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPE_CHOICES)
    config = models.JSONField()  # Chart.js or other visualization config
    data = models.JSONField()  # Chart data
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_visualization'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.chart_type})"