export type BookStatus = 'available' | 'borrowed' | 'archived';

export interface Book {
	id: number;
	title: string;
	original_title: string | null;
	author: string;
	publisher: string | null;
	original_pub_date: string | null;
	publishing_date: string | null;
	edition_date: string | null;
	language: string | null;
	original_language: string | null;
	cover_image_path: string | null;
	status: BookStatus;
	notes: string | null;
	created_at: string;
	updated_at: string;
}

export interface BookCreate {
	title: string;
	original_title?: string | null;
	author: string;
	publisher?: string | null;
	original_pub_date?: string | null;
	publishing_date?: string | null;
	edition_date?: string | null;
	language?: string | null;
	original_language?: string | null;
	status?: BookStatus;
	notes?: string | null;
}

export interface BookUpdate {
	title?: string | null;
	original_title?: string | null;
	author?: string | null;
	publisher?: string | null;
	original_pub_date?: string | null;
	publishing_date?: string | null;
	edition_date?: string | null;
	language?: string | null;
	original_language?: string | null;
	status?: BookStatus | null;
	notes?: string | null;
}

export interface OCRResult {
	title: string | null;
	original_title: string | null;
	author: string | null;
	publisher: string | null;
	original_pub_date: string | null;
	publishing_date: string | null;
	language: string | null;
	raw_text: string;
}

export interface BookStats {
	total: number;
	available: number;
	borrowed: number;
	archived: number;
}
