import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Dataset } from '../../services/dataset';
import { JsonPipe } from '@angular/common';

@Component({
  selector: 'app-datasets',
  standalone: true,
  imports: [JsonPipe],
  templateUrl: './datasets.html',
  styleUrl: './datasets.css',
})
export class Datasets implements OnInit {
  datasets: any[] = [];
  message = 'Loading datasets...';
  selectedFile: File | null = null;
  isUploading = false;

  constructor(
    private datasetService: Dataset,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.loadDatasets();
  }

  loadDatasets(): void {
    this.datasetService.getMyDatasets().subscribe({
      next: (response) => {
        this.datasets = response.datasets;
        this.message = this.datasets.length === 0 ? 'No datasets uploaded yet.' : '';

        this.cdr.detectChanges();
      },

      error: (error) => {
        console.error(error);
        this.message = 'Failed to load datasets.';
        this.cdr.detectChanges();
      },
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFile = input.files?.[0] ?? null;
    this.message = '';
  }

  uploadDataset(): void {
    if (!this.selectedFile) {
      this.message = 'Please select a CSV or Excel file.';
      return;
    }

    const allowedExtensions = ['csv', 'xlsx', 'xls'];
    const extension = this.selectedFile.name.split('.').pop()?.toLowerCase();

    if (!extension || !allowedExtensions.includes(extension)) {
      this.message = 'Only CSV and Excel files are allowed.';
      return;
    }

    const fileToUpload = this.selectedFile;

    this.isUploading = true;
    this.message = 'Uploading dataset...';

    this.datasetService.uploadDataset(fileToUpload).subscribe({
      next: () => {
        this.isUploading = false;
        this.selectedFile = null;
        this.message = 'Dataset uploaded successfully!';

        this.cdr.detectChanges();
        this.loadDatasets();
      },

      error: (error) => {
        console.error('Upload error:', error);

        this.isUploading = false;
        this.message = error.error?.detail || 'Dataset upload failed.';

        this.cdr.detectChanges();
      },
    });
  }
  selectedDatasetId: number | null = null;
  datasetProfile: any = null;
  isLoadingProfile = false;
  profileMessage = '';

  viewDetails(datasetId: number): void {
    this.selectedDatasetId = datasetId;
    this.datasetProfile = null;
    this.isLoadingProfile = true;
    this.profileMessage = '';

    this.datasetService.getDatasetProfile(datasetId).subscribe({
      next: (response) => {
        this.datasetProfile = response;
        this.isLoadingProfile = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Profile error:', error);
        this.isLoadingProfile = false;
        this.profileMessage = 'Failed to load dataset profile.';
        this.cdr.detectChanges();
      },
    });
  }
}
