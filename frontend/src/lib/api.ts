import type { Book, BookCreate, BookStats, BookStatus, BookUpdate, ImportResult, LibraryStats, OCRResult } from './types';

const BASE = '';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
	const res = await fetch(`${BASE}${url}`, {
		headers: { 'Content-Type': 'application/json', ...options?.headers },
		...options
	});
	if (!res.ok) {
		const body = await res.text();
		throw new Error(`${res.status}: ${body}`);
	}
	if (res.status === 204) return undefined as T;
	return res.json();
}

export const api = {
	books: {
		list(params?: { status?: BookStatus; search?: string }): Promise<Book[]> {
			const sp = new URLSearchParams();
			if (params?.status) sp.set('status', params.status);
			if (params?.search) sp.set('search', params.search);
			const qs = sp.toString();
			return request(`/api/books${qs ? `?${qs}` : ''}`);
		},
		get(id: number): Promise<Book> {
			return request(`/api/books/${id}`);
		},
		create(data: BookCreate): Promise<Book> {
			return request('/api/books', { method: 'POST', body: JSON.stringify(data) });
		},
		update(id: number, data: BookUpdate): Promise<Book> {
			return request(`/api/books/${id}`, { method: 'PUT', body: JSON.stringify(data) });
		},
		delete(id: number): Promise<void> {
			return request(`/api/books/${id}`, { method: 'DELETE' });
		},
		updateStatus(id: number, status: BookStatus): Promise<Book> {
			return request(`/api/books/${id}/status`, {
				method: 'PATCH',
				body: JSON.stringify({ status })
			});
		},
		borrow(id: number, borrowerName: string): Promise<Book> {
			return request(`/api/books/${id}/borrow`, {
				method: 'POST',
				body: JSON.stringify({ borrower_name: borrowerName })
			});
		},
		async uploadCover(id: number, file: File): Promise<Book> {
			const form = new FormData();
			form.append('file', file);
			const res = await fetch(`${BASE}/api/books/${id}/cover`, {
				method: 'POST',
				body: form
			});
			if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
			return res.json();
		},
		fetchCover(id: number): Promise<Book> {
			return request(`/api/books/${id}/fetch-cover`, { method: 'POST' });
		},
		stats(): Promise<BookStats> {
			return request('/api/books/stats');
		},
		libraryStats(): Promise<LibraryStats> {
			return request('/api/books/library-stats');
		}
	},
	borrowed: {
		list(search?: string): Promise<Book[]> {
			const sp = new URLSearchParams();
			if (search) sp.set('search', search);
			const qs = sp.toString();
			return request(`/api/borrowed${qs ? `?${qs}` : ''}`);
		}
	},
	archived: {
		list(search?: string): Promise<Book[]> {
			const sp = new URLSearchParams();
			if (search) sp.set('search', search);
			const qs = sp.toString();
			return request(`/api/archived${qs ? `?${qs}` : ''}`);
		}
	},
	ocr: {
		async extract(files: File[]): Promise<OCRResult> {
			const form = new FormData();
			for (const f of files) form.append('files', f);
			const res = await fetch(`${BASE}/api/ocr/extract`, {
				method: 'POST',
				body: form
			});
			if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
			return res.json();
		}
	},
	data: {
		async importCsv(file: File): Promise<ImportResult> {
			const form = new FormData();
			form.append('file', file);
			const res = await fetch(`${BASE}/api/data/import-csv`, {
				method: 'POST',
				body: form
			});
			if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
			return res.json();
		},
		exportUrl(format: string = 'json'): string {
			return `${BASE}/api/data/export?format=${encodeURIComponent(format)}`;
		},
		backupUrl(): string {
			return `${BASE}/api/data/backup`;
		}
	}
};
