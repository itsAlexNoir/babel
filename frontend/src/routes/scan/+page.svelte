<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import type { BookCreate, OCRResult } from '$lib/types';
	import ImageUpload from '$lib/components/ImageUpload.svelte';
	import BookForm from '$lib/components/BookForm.svelte';
	import { toast } from '$lib/toast';

	let files: File[] = $state([]);
	let scanning = $state(false);
	let result: OCRResult | null = $state(null);
	let saving = $state(false);

	async function handleScan() {
		if (files.length === 0) return;
		scanning = true;
		try {
			result = await api.ocr.extract(files);
			toast('Text extracted! Review and edit the fields below.', 'info');
		} catch {
			toast('Failed to extract text from images.', 'error');
		}
		scanning = false;
	}

	async function handleSave(data: BookCreate) {
		saving = true;
		try {
			const book = await api.books.create(data);
			toast('Book added from scan!', 'success');
			goto(`/books/${book.id}`);
		} catch {
			toast('Failed to save book.', 'error');
		}
		saving = false;
	}

	function reset() {
		files = [];
		result = null;
	}
</script>

<div class="page-header">
	<h1>Scan Book</h1>
</div>

<p class="description">
	Upload one or more photos of a book (cover, title page, copyright page) and the app will
	extract the book information using OCR. Review and correct the results before saving.
</p>

<div class="tip">
	💡 <strong>Tips for better results:</strong> Use well-lit, flat photos. Title pages and copyright pages contain the most useful data.
</div>

{#if !result}
	<div class="upload-section">
		<ImageUpload bind:files />
		{#if files.length > 0}
			<button class="primary scan-btn" onclick={handleScan} disabled={scanning}>
				{scanning ? 'Scanning...' : `Scan ${files.length} image${files.length > 1 ? 's' : ''}`}
			</button>
		{/if}
	</div>
{:else}
	<div class="result-section">
		{#if result.raw_text}
			<details class="raw-text">
				<summary>View raw OCR text</summary>
				<pre>{result.raw_text}</pre>
			</details>
		{/if}

		<h2>Review & Save</h2>
		<div class="form-container">
			<BookForm
				initial={{
					title: result.title ?? '',
					author: result.author ?? '',
					publisher: result.publisher ?? undefined,
					original_pub_date: result.original_pub_date ?? undefined,
					publishing_date: result.publishing_date ?? undefined,
					language: result.language ?? undefined,
				}}
				submitLabel={saving ? 'Saving...' : 'Save Book'}
				onSubmit={handleSave}
				onCancel={reset}
			/>
		</div>
	</div>
{/if}

<style>
	.page-header {
		margin-bottom: 0.75rem;
	}

	h1 {
		font-size: 1.5rem;
		font-weight: 600;
	}

	h2 {
		font-size: 1.15rem;
		font-weight: 600;
		margin-bottom: 1rem;
	}

	.description {
		color: var(--color-text-secondary);
		font-size: 0.9rem;
		margin-bottom: 1rem;
	}

	.tip {
		background: var(--color-badge-borrowed);
		border: 1px solid var(--color-warning);
		border-radius: var(--radius);
		padding: 0.75rem 1rem;
		font-size: 0.85rem;
		margin-bottom: 1.5rem;
	}

	.upload-section {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		max-width: 600px;
	}

	.scan-btn {
		align-self: flex-start;
	}

	.result-section {
		max-width: 800px;
	}

	.raw-text {
		margin-bottom: 1.5rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 0.75rem;
	}

	.raw-text summary {
		cursor: pointer;
		font-size: 0.85rem;
		font-weight: 500;
		color: var(--color-text-secondary);
	}

	.raw-text pre {
		margin-top: 0.75rem;
		font-size: 0.8rem;
		white-space: pre-wrap;
		word-break: break-word;
		max-height: 200px;
		overflow-y: auto;
	}

	.form-container {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1.5rem;
	}
</style>
