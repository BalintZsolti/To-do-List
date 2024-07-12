import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private baseUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  getTasks(): Observable<any> {
    return this.http.get(`${this.baseUrl}/tasks/`);
  }

  createTask(task: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/tasks/`, task);
  }

  editTask(taskId: string, task: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/tasks/${taskId}`, task);
  }

  deleteTask(taskId: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/tasks/${taskId}`);
  }
}
