import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DatasetResponse {
  user_id: number;
  total_datasets: number;
  datasets: any[];
}

@Injectable({
  providedIn: 'root',
})
export class Dataset {
  private apiUrl = 'http://127.0.0.1:8000/datasets';

  constructor(private http: HttpClient) {}

  getMyDatasets(): Observable<DatasetResponse> {
    return this.http.get<DatasetResponse>(`${this.apiUrl}/my`);
  }

  uploadDataset(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(`${this.apiUrl}/upload`, formData);
  }

  getDatasetProfile(datasetId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${datasetId}/profile`);
  }
}
