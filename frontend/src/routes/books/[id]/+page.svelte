<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { Book, BookCreate } from '$lib/types';
	import BookForm from '$lib/components/BookForm.svelte';
	import { toast } from '$lib/toast';

	let book: Book | null = $state(null);
	let editing = $state(false);
	let loading = $state(true);
	let coverFile: FileList | null = $state(null);
	let fetchingCover = $state(false);
	let confirmDelete = $state(false);
	let borrowing = $state(false);
	let borrowerName = $state('');
	let editingBorrowedAt = $state(false);
	let editingArchivedAt = $state(false);
	let borrowedAtValue = $state('');
	let archivedAtValue = $state('');

	const bookId = $derived(Number(page.params.id));

	async function load() {
		loading = true;
		try {
			book = await api.books.get(bookId);
		} catch {
			toast('Book not found.', 'error');
			goto('/books');
		}
		loading = false;
	}

	onMount(load);

	async function handleUpdate(data: BookCreate) {
		if (!book) return;
		try {
			book = await api.books.update(book.id, data);
			editing = false;
			toast('Book updated.', 'success');
		} catch {
			toast('Failed to update book.', 'error');
		}
	}

	async function handleDelete() {
		if (!book) return;
		try {
			await api.books.delete(book.id);
			toast('Book deleted.', 'success');
			goto('/books');
		} catch {
			toast('Failed to delete book.', 'error');
		}
	}

	async function handleStatusChange(status: 'available' | 'borrowed' | 'archived') {
		if (!book) return;
		try {
			book = await api.books.updateStatus(book.id, status);
			toast(`Book marked as ${status}.`, 'success');
		} catch {
			toast('Failed to update status.', 'error');
		}
	}

	async function handleBorrow() {
		if (!book || !borrowerName.trim()) return;
		try {
			book = await api.books.borrow(book.id, borrowerName.trim());
			borrowing = false;
			borrowerName = '';
			toast(`Lent to ${book.borrower_name}.`, 'success');
		} catch {
			toast('Failed to mark as borrowed.', 'error');
		}
	}

	async function handleCoverUpload() {
		if (!book || !coverFile || !coverFile[0]) return;
		try {
			book = await api.books.uploadCover(book.id, coverFile[0]);
			coverFile = null;
			toast('Cover uploaded.', 'success');
		} catch {
			toast('Failed to upload cover.', 'error');
		}
	}

	async function handleFetchCover() {
		if (!book) return;
		fetchingCover = true;
		try {
			book = await api.books.fetchCover(book.id);
			toast('Cover fetched from Open Library.', 'success');
		} catch {
			toast('Cover not found on Open Library.', 'error');
		}
		fetchingCover = false;
	}

	function toDateInputValue(iso: string | null): string {
		return iso ? iso.slice(0, 10) : '';
	}

	async function handleDateUpdate(field: 'borrowed_at' | 'archived_at', value: string) {
		if (!book) return;
		try {
			book = await api.books.update(book.id, { [field]: value ? value + 'T00:00:00' : null });
			toast('Date updated.', 'success');
		} catch {
			toast('Failed to update date.', 'error');
		}
		if (field === 'borrowed_at') editingBorrowedAt = false;
		else editingArchivedAt = false;
	}

	function getCoverUrl(b: Book | null): string | null {
		return b?.cover_image_path ? `/uploads/${b.cover_image_path}` : null;
	}
</script>

{#if loading}
	<p class="loading">Loading...</p>
{:else if book}
	{@const coverUrl = getCoverUrl(book)}
	{#if editing}
		<div class="page-header">
			<h1>Edit Book</h1>
		</div>
		<div class="form-container">
			<BookForm
				initial={book}
				submitLabel="Update Book"
				onSubmit={handleUpdate}
				onCancel={() => editing = false}
			/>
		</div>
	{:else}
		<div class="page-header">
			<h1>{book.title}</h1>
			<div class="header-actions">
				<button onclick={() => editing = true}>Edit</button>
				{#if confirmDelete}
					<button class="danger" onclick={handleDelete}>Confirm Delete</button>
					<button onclick={() => confirmDelete = false}>Cancel</button>
				{:else}
					<button class="danger" onclick={() => confirmDelete = true}>Delete</button>
				{/if}
			</div>
		</div>

		<div class="detail-layout">
			<div class="cover-section">
				{#if coverUrl}
					<img src={coverUrl} alt="{book.title} cover" class="cover-img" />
				{:else}
					<div class="cover-placeholder">
						<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>
						<span>No cover</span>
					</div>
				{/if}
				<div class="cover-actions">
					<button class="small" onclick={handleFetchCover} disabled={fetchingCover}>
						{fetchingCover ? 'Fetching...' : 'Fetch Cover'}
					</button>
					<label class="upload-label small">
						Upload
						<input type="file" accept="image/*" bind:files={coverFile} onchange={handleCoverUpload} hidden />
					</label>
				</div>
			</div>

			<div class="info-section">
				<div class="info-grid">
					{#if book.original_title}
						<div class="info-item">
							<span class="info-label">Original Title</span>
							<span class="info-value">{book.original_title}</span>
						</div>
					{/if}
					<div class="info-item">
						<span class="info-label">Author</span>
						<span class="info-value">{book.author}</span>
					</div>
					{#if book.publisher}
						<div class="info-item">
							<span class="info-label">Publisher</span>
							<span class="info-value">{book.publisher}</span>
						</div>
					{/if}
					{#if book.original_pub_date}
						<div class="info-item">
							<span class="info-label">Original Publication</span>
							<span class="info-value">{book.original_pub_date}</span>
						</div>
					{/if}
					{#if book.publishing_date}
						<div class="info-item">
							<span class="info-label">Publishing Date</span>
							<span class="info-value">{book.publishing_date}</span>
						</div>
					{/if}
					{#if book.edition_date}
						<div class="info-item">
							<span class="info-label">Edition Date</span>
							<span class="info-value">{book.edition_date}</span>
						</div>
					{/if}
					{#if book.language}
						<div class="info-item">
							<span class="info-label">Language</span>
							<span class="info-value">{book.language}</span>
						</div>
					{/if}
					{#if book.original_language}
						<div class="info-item">
							<span class="info-label">Original Language</span>
							<span class="info-value">{book.original_language}</span>
						</div>
					{/if}
					{#if book.translator}
						<div class="info-item">
							<span class="info-label">Translator</span>
							<span class="info-value">{book.translator}</span>
						</div>
					{/if}
				<div class="info-item">
					<span class="info-label">Entry Date</span>
					<span class="info-value">{new Date(book.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}</span>
				</div>
						{#if book.status === 'available'}
							{#if borrowing}
								<form class="borrow-form" onsubmit={(e) => { e.preventDefault(); handleBorrow(); }}>
									<input
										type="text"
										placeholder="Borrower's name"
										bind:value={borrowerName}
										autofocus
										required
									/>
									<button type="submit" class="primary small">Confirm</button>
									<button type="button" class="small" onclick={() => { borrowing = false; borrowerName = ''; }}>Cancel</button>
								</form>
							{:else}
								<button class="small" onclick={() => borrowing = true}>Mark Borrowed</button>
								<button class="small" onclick={() => handleStatusChange('archived')}>Archive</button>
							{/if}
						{:else if book.status === 'borrowed'}
							<div class="borrow-info">
								<span class="borrow-person">{book.borrower_name ?? 'Unknown'}</span>
								{#if editingBorrowedAt}
									<form class="date-edit-form" onsubmit={(e) => { e.preventDefault(); handleDateUpdate('borrowed_at', borrowedAtValue); }}>
										<input type="date" bind:value={borrowedAtValue} />
										<button type="submit" class="primary small">Save</button>
										<button type="button" class="small" onclick={() => editingBorrowedAt = false}>Cancel</button>
									</form>
								{:else if book.borrowed_at}
									<span class="borrow-date">
										since {new Date(book.borrowed_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
										<button class="icon-btn" type="button" onclick={() => { borrowedAtValue = toDateInputValue(book!.borrowed_at); editingBorrowedAt = true; }} title="Edit date">✎</button>
									</span>
								{/if}
							</div>
							<button class="small" onclick={() => handleStatusChange('available')}>Return</button>
						{:else if book.status === 'archived'}
							{#if editingArchivedAt}
								<form class="date-edit-form" onsubmit={(e) => { e.preventDefault(); handleDateUpdate('archived_at', archivedAtValue); }}>
									<input type="date" bind:value={archivedAtValue} />
									<button type="submit" class="primary small">Save</button>
									<button type="button" class="small" onclick={() => editingArchivedAt = false}>Cancel</button>
								</form>
							{:else if book.archived_at}
								<span class="borrow-date">
									since {new Date(book.archived_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
									<button class="icon-btn" type="button" onclick={() => { archivedAtValue = toDateInputValue(book!.archived_at); editingArchivedAt = true; }} title="Edit date">✎</button>
								</span>
							{/if}
							<button class="small" onclick={() => handleStatusChange('available')}>Restore</button>
						{/if}
					</div>

				{#if book.notes}
					<div class="notes-section">
						<span class="info-label">Notes</span>
						<p class="notes-text">{book.notes}</p>
					</div>
				{/if}
				{#if book.tags}
					<div class="notes-section">
						<span class="info-label">Tags</span>
						<div class="tags-list">
							{#each book.tags.split(';') as tag}
								<span class="tag">{tag.trim()}</span>
							{/each}
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}
{/if}

<style>
	.page-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 1.5rem;
		flex-wrap: wrap;
		gap: 0.75rem;
	}

	h1 {
		font-size: 1.5rem;
		font-weight: 600;
	}

	.header-actions {
		display: flex;
		gap: 0.5rem;
	}

	.detail-layout {
		display: flex;
		gap: 2rem;
	}

	.cover-section {
		flex-shrink: 0;
		width: 200px;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.cover-img {
		width: 100%;
		border-radius: var(--radius);
		border: 1px solid var(--color-border);
	}

	.cover-placeholder {
		width: 100%;
		aspect-ratio: 2 / 3;
		background: var(--color-bg);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		color: var(--color-border);
		font-size: 0.8rem;
	}

	.cover-actions {
		display: flex;
		gap: 0.5rem;
	}

	.upload-label {
		cursor: pointer;
		padding: 0.25rem 0.75rem;
		font-size: 0.8rem;
		font-weight: 500;
		border-radius: var(--radius);
		border: 1px solid var(--color-border);
		background: var(--color-surface);
		transition: all 0.15s ease;
		text-align: center;
	}

	.upload-label:hover {
		background: var(--color-bg);
	}

	.info-section {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.info-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1rem;
	}

	.info-item {
		display: flex;
		flex-direction: column;
		gap: 0.125rem;
	}

	.info-label {
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.025em;
	}

	.info-value {
		font-size: 0.95rem;
	}

	.status-section {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.status-controls {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		flex-wrap: wrap;
	}

	.borrow-form {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.borrow-form input {
		font-family: inherit;
		font-size: 0.875rem;
		padding: 0.35rem 0.65rem;
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		outline: none;
		min-width: 180px;
	}

	.borrow-form input:focus {
		border-color: var(--color-primary);
	}

	.borrow-info {
		display: flex;
		flex-direction: column;
		gap: 0.1rem;
	}

	.borrow-person {
		font-weight: 600;
		font-size: 0.9rem;
	}

	.borrow-date {
		font-size: 0.8rem;
		color: var(--color-text-secondary);
		display: flex;
		align-items: center;
		gap: 0.3rem;
	}

	.icon-btn {
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		font-size: 0.85rem;
		color: var(--color-text-secondary);
		line-height: 1;
		opacity: 0.5;
		transition: opacity 0.15s;
	}

	.icon-btn:hover {
		opacity: 1;
	}

	.date-edit-form {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		flex-wrap: wrap;
	}

	.date-edit-form input[type='date'] {
		font-family: inherit;
		font-size: 0.8rem;
		padding: 0.25rem 0.5rem;
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		outline: none;
	}

	.date-edit-form input[type='date']:focus {
		border-color: var(--color-primary);
	}

	.notes-text {
		font-size: 0.9rem;
		color: var(--color-text-secondary);
		line-height: 1.6;
		margin-top: 0.25rem;
	}

	.tags-list {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
		margin-top: 0.25rem;
	}

	.tag {
		font-size: 0.75rem;
		padding: 0.2rem 0.6rem;
		background: var(--color-bg);
		border: 1px solid var(--color-border);
		border-radius: 999px;
		color: var(--color-text-secondary);
	}

	.form-container {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1.5rem;
		max-width: 800px;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: var(--color-text-secondary);
	}

	@media (max-width: 640px) {
		.detail-layout {
			flex-direction: column;
		}

		.cover-section {
			width: 150px;
		}

		.info-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
