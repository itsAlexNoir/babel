<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { Book, BookCreate } from '$lib/types';
	import BookForm from '$lib/components/BookForm.svelte';
	import BookCover from '$lib/components/BookCover.svelte';
	import BorrowDialog from '$lib/components/BorrowDialog.svelte';
	import { toast } from '$lib/toast';

	let book: Book | null = $state(null);
	let editing = $state(false);
	let loading = $state(true);
	let coverFile: FileList | null = $state(null);
	let fetchingCover = $state(false);
	let borrowing = $state(false);
	let menuOpen = $state(false);
	let confirmDeleteOpen = $state(false);
	let editingBorrowedAt = $state(false);
	let editingArchivedAt = $state(false);
	let borrowedAtValue = $state('');
	let archivedAtValue = $state('');
	let deleteDialogEl: HTMLDialogElement | undefined = $state();

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

	$effect(() => {
		if (confirmDeleteOpen) deleteDialogEl?.showModal();
		else deleteDialogEl?.close();
	});

	function closeMenu() {
		menuOpen = false;
	}

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
			confirmDeleteOpen = false;
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

	async function handleBorrowConfirm(borrowerName: string) {
		if (!book) return;
		try {
			book = await api.books.borrow(book.id, borrowerName);
			borrowing = false;
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
		closeMenu();
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

	const tags = $derived.by(() => {
		const b = book;
		return b?.tags ? b.tags.split(';').map((t: string) => t.trim()).filter(Boolean) : [];
	});
</script>

{#if loading}
	<p class="loading">Loading…</p>
{:else if book}
	{#if editing}
		<div class="page-header">
			<h1>Edit book</h1>
		</div>
		<div class="form-container">
			<BookForm initial={book} submitLabel="Update book" onSubmit={handleUpdate} onCancel={() => (editing = false)} />
		</div>
	{:else}
		<div class="crumb">
			<a href="/books" class="back" aria-label="Back to catalogue">
				<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>
			</a>
			<a href="/books">Catalogue</a>
			{#if tags[0]}
				<span class="sep">/</span>
				<a href="/books?tags={encodeURIComponent(tags[0])}">{tags[0]}</a>
			{/if}
			<div class="spacer"></div>
			<button onclick={() => (editing = true)}>
				<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
				Edit
			</button>
			<div class="menu-wrap">
				<button class="icon-only" onclick={() => (menuOpen = !menuOpen)} aria-label="More actions">
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="5" cy="12" r="1.4" fill="currentColor"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/><circle cx="19" cy="12" r="1.4" fill="currentColor"/></svg>
				</button>
				{#if menuOpen}
					<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
					<div class="menu-backdrop" onclick={closeMenu}></div>
					<div class="menu">
						<button onclick={handleFetchCover} disabled={fetchingCover}>
							{fetchingCover ? 'Fetching cover…' : 'Fetch cover art'}
						</button>
						<div class="menu-rule"></div>
						<button class="danger-item" onclick={() => { menuOpen = false; confirmDeleteOpen = true; }}>Delete book…</button>
					</div>
				{/if}
			</div>
		</div>

		<div class="detail-layout">
			<div class="cover-section">
				<div class="cover-frame"><BookCover {book} size="l" /></div>
				<div class="cover-actions">
					<button class="small" onclick={handleFetchCover} disabled={fetchingCover}>
						{fetchingCover ? 'Fetching…' : 'Fetch cover'}
					</button>
					<label class="upload-label small">
						Upload…
						<input type="file" accept="image/*" bind:files={coverFile} onchange={handleCoverUpload} hidden />
					</label>
				</div>
				{#if !book.cover_image_path}
					<p class="cover-hint">No cover on file — set from title, author and publisher.</p>
				{/if}
			</div>

			<div class="info-section">
				<div class="titleblock">
					<h1>{book.title}</h1>
					{#if book.original_title && book.original_title !== book.title}
						<p class="original-title">{book.original_title}</p>
					{/if}
					<p class="byline">
						{book.author}{#if book.translator} &nbsp;·&nbsp; translated by {book.translator}{/if}
					</p>
				</div>

				<div class="status-bar">
					{#if book.status === 'available'}
						<span class="stat" style="color: var(--color-avail)"><span class="dot"></span>On the shelf</span>
					{:else if book.status === 'borrowed'}
						<span class="stat out"><span class="dot"></span>{book.borrower_name ?? 'Unknown'}</span>
					{:else}
						<span class="stat arch">Archived</span>
					{/if}

					{#if book.status === 'borrowed'}
						{#if editingBorrowedAt}
							<form class="date-edit-form" onsubmit={(e) => { e.preventDefault(); handleDateUpdate('borrowed_at', borrowedAtValue); }}>
								<input type="date" bind:value={borrowedAtValue} />
								<button type="submit" class="primary small">Save</button>
								<button type="button" class="small" onclick={() => (editingBorrowedAt = false)}>Cancel</button>
							</form>
						{:else if book.borrowed_at}
							<span class="date-note">
								since <span class="mono">{new Date(book.borrowed_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}</span>
								<button class="icon-btn" type="button" onclick={() => { borrowedAtValue = toDateInputValue(book!.borrowed_at); editingBorrowedAt = true; }} title="Edit date">✎</button>
							</span>
						{/if}
					{:else if book.status === 'archived'}
						{#if editingArchivedAt}
							<form class="date-edit-form" onsubmit={(e) => { e.preventDefault(); handleDateUpdate('archived_at', archivedAtValue); }}>
								<input type="date" bind:value={archivedAtValue} />
								<button type="submit" class="primary small">Save</button>
								<button type="button" class="small" onclick={() => (editingArchivedAt = false)}>Cancel</button>
							</form>
						{:else if book.archived_at}
							<span class="date-note">
								since <span class="mono">{new Date(book.archived_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}</span>
								<button class="icon-btn" type="button" onclick={() => { archivedAtValue = toDateInputValue(book!.archived_at); editingArchivedAt = true; }} title="Edit date">✎</button>
							</span>
						{/if}
					{/if}

					<div class="spacer"></div>

					{#if book.status === 'available'}
						<button class="small" onclick={() => handleStatusChange('archived')}>Archive</button>
						<button class="primary small" onclick={() => (borrowing = true)}>Lend this book</button>
					{:else if book.status === 'borrowed'}
						<button class="small" onclick={() => handleStatusChange('available')}>Return</button>
					{:else if book.status === 'archived'}
						<button class="small" onclick={() => handleStatusChange('available')}>Restore</button>
					{/if}
				</div>

				<div class="info-grid">
					<div class="info-item">
						<span class="info-label">Author</span>
						<span class="info-value">{book.author}</span>
					</div>
					{#if book.translator}
						<div class="info-item">
							<span class="info-label">Translator</span>
							<span class="info-value">{book.translator}</span>
						</div>
					{/if}
					{#if book.original_title}
						<div class="info-item">
							<span class="info-label">Original title</span>
							<span class="info-value italic">{book.original_title}</span>
						</div>
					{/if}
					{#if book.original_language}
						<div class="info-item">
							<span class="info-label">Original language</span>
							<span class="info-value">{book.original_language}</span>
						</div>
					{/if}
					{#if book.publisher}
						<div class="info-item">
							<span class="info-label">Publisher</span>
							<span class="info-value">{book.publisher}</span>
						</div>
					{/if}
					{#if book.language}
						<div class="info-item">
							<span class="info-label">Language</span>
							<span class="info-value">{book.language}</span>
						</div>
					{/if}
					{#if book.original_pub_date}
						<div class="info-item">
							<span class="info-label">First published</span>
							<span class="info-value mono">{book.original_pub_date}</span>
						</div>
					{/if}
					{#if book.publishing_date}
						<div class="info-item">
							<span class="info-label">This edition</span>
							<span class="info-value mono">{book.publishing_date}</span>
						</div>
					{/if}
					{#if book.edition_date}
						<div class="info-item">
							<span class="info-label">Edition date</span>
							<span class="info-value mono">{book.edition_date}</span>
						</div>
					{/if}
					<div class="info-item">
						<span class="info-label">Added to library</span>
						<span class="info-value mono">{new Date(book.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}</span>
					</div>
				</div>

				<div class="lower-grid">
					{#if tags.length}
						<div class="lower-col">
							<span class="eyebrow">Tags</span>
							<div class="tags-list">
								{#each tags as tag}
									<a href="/books?tags={encodeURIComponent(tag)}" class="tag">{tag}</a>
								{/each}
							</div>
						</div>
					{/if}
					{#if book.notes}
						<div class="lower-col wide">
							<span class="eyebrow">Notes</span>
							<p class="notes-text">{book.notes}</p>
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
{/if}

<BorrowDialog book={borrowing ? book : null} onConfirm={handleBorrowConfirm} onClose={() => (borrowing = false)} />

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<dialog bind:this={deleteDialogEl} onclose={() => (confirmDeleteOpen = false)} onclick={(e) => { if (e.target === deleteDialogEl) confirmDeleteOpen = false; }}>
	{#if book}
		<h2>Delete <em>{book.title}</em>?</h2>
		<p class="delete-copy">This removes the book, its cover and its lending history. It cannot be undone.</p>
		<div class="rule"></div>
		<div class="dialog-actions">
			<button onclick={() => (confirmDeleteOpen = false)}>Cancel</button>
			<button class="danger" onclick={handleDelete}>Delete book</button>
		</div>
	{/if}
</dialog>

<style>
	.crumb {
		display: flex;
		align-items: center;
		gap: 9px;
		font-size: 12.5px;
		color: var(--color-muted);
		padding: 2px 0 20px;
	}

	.back {
		display: flex;
		color: var(--color-faint);
	}

	.crumb a {
		color: var(--color-muted);
	}

	.crumb a:hover {
		color: var(--color-spot);
	}

	.sep {
		color: var(--color-rule-strong);
	}

	.spacer {
		flex: 1;
	}

	.menu-wrap {
		position: relative;
	}

	.icon-only {
		width: 31px;
		padding: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.menu-backdrop {
		position: fixed;
		inset: 0;
		z-index: 19;
	}

	.menu {
		position: absolute;
		top: calc(100% + 6px);
		right: 0;
		z-index: 20;
		width: 210px;
		background: var(--color-paper);
		border: 1px solid var(--color-ink);
		box-shadow: var(--shadow);
		padding: 5px;
	}

	.menu button {
		display: flex;
		width: 100%;
		height: 30px;
		align-items: center;
		padding: 0 10px;
		border: none;
		border-radius: 0;
		background: transparent;
		font-size: 13px;
		color: var(--color-sub);
		text-align: left;
	}

	.menu button:hover {
		background: var(--color-rule-faint);
		color: var(--color-ink);
	}

	.menu-rule {
		height: 1px;
		background: var(--color-rule-faint);
		margin: 5px 10px;
	}

	.danger-item {
		color: var(--color-danger) !important;
		font-weight: 500;
	}

	.detail-layout {
		display: flex;
		gap: 52px;
	}

	.cover-section {
		flex-shrink: 0;
		width: 252px;
		display: flex;
		flex-direction: column;
		gap: 13px;
	}

	.cover-frame {
		width: 100%;
	}

	.cover-actions {
		display: flex;
		gap: 7px;
	}

	.cover-actions .small {
		flex: 1;
	}

	/* A <label> wrapping a hidden file input, styled to match button.small —
	   the global `label` rule (form-field captions) does not apply to buttons,
	   so every property it sets has to be reset here explicitly. */
	.upload-label {
		cursor: pointer;
		display: flex;
		flex: 1;
		align-items: center;
		justify-content: center;
		text-align: center;
		height: 26px;
		padding: 0 10px;
		border: 1px solid var(--color-rule);
		border-radius: var(--radius);
		font-size: 11.5px;
		font-weight: 500;
		letter-spacing: normal;
		text-transform: none;
		color: var(--color-sub);
		margin-bottom: 0;
	}

	.upload-label:hover {
		border-color: var(--color-rule-strong);
		color: var(--color-ink);
		background: var(--color-paper-2);
	}

	.cover-hint {
		font-size: 11px;
		color: var(--color-faint);
		line-height: 1.5;
	}

	.info-section {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
		gap: 24px;
	}

	.titleblock h1 {
		font-size: 44px;
		line-height: 1.08;
		letter-spacing: -0.012em;
	}

	.original-title {
		font-family: var(--font-serif);
		font-style: italic;
		font-size: 24px;
		line-height: 1.2;
		color: var(--color-faint);
		margin-top: 3px;
	}

	.byline {
		font-size: 13.5px;
		color: var(--color-muted);
		margin-top: 11px;
	}

	.status-bar {
		display: flex;
		align-items: center;
		gap: 16px;
		flex-wrap: wrap;
		padding: 13px 0;
		border-top: 1px solid var(--color-ink);
		border-bottom: 1px solid var(--color-rule);
	}

	.date-note {
		font-size: 12px;
		color: var(--color-muted);
		display: flex;
		align-items: center;
		gap: 5px;
	}

	.icon-btn {
		background: none;
		border: none;
		padding: 0;
		height: auto;
		cursor: pointer;
		font-size: 0.8rem;
		color: var(--color-muted);
		line-height: 1;
		opacity: 0.55;
	}

	.icon-btn:hover {
		background: none;
		border: none;
		opacity: 1;
	}

	.date-edit-form {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		flex-wrap: wrap;
	}

	.date-edit-form input[type='date'] {
		width: auto;
		font-size: 0.8rem;
	}

	.info-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0 52px;
	}

	.info-item {
		display: flex;
		gap: 18px;
		padding: 9px 0;
		border-bottom: 1px solid var(--color-rule-faint);
	}

	.info-label {
		width: 132px;
		flex: none;
		font-size: 10px;
		font-weight: 600;
		letter-spacing: 0.09em;
		text-transform: uppercase;
		color: var(--color-faint);
		padding-top: 2px;
	}

	.info-value {
		font-size: 13.5px;
		color: var(--color-ink);
	}

	.info-value.italic {
		font-style: italic;
	}

	.lower-grid {
		display: flex;
		gap: 52px;
		flex-wrap: wrap;
	}

	.lower-col {
		display: flex;
		flex-direction: column;
		gap: 9px;
		flex: 1;
		min-width: 220px;
	}

	.lower-col.wide {
		flex: 1.6;
	}

	.tags-list {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}

	.notes-text {
		font-size: 13.5px;
		line-height: 1.62;
		color: var(--color-sub);
		max-width: 60ch;
	}

	.form-container {
		background: var(--color-paper);
		border: 1px solid var(--color-rule);
		padding: 1.5rem;
		max-width: 800px;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: var(--color-muted);
	}

	/* Delete confirmation dialog */
	dialog {
		/* The global `* { margin: 0 }` reset clobbers the UA stylesheet's
		   `margin: auto`, which is what centers a modal <dialog> — restore it.
		   The UA stylesheet also sets `color: black` on <dialog> itself (not
		   just as a default), which blocks inheritance from body and stayed
		   invisible in light mode since black ≈ --color-ink there — reset it
		   explicitly or every descendant renders black text in dark mode. */
		margin: auto;
		color: var(--color-ink);
		border: 1px solid var(--color-ink);
		border-radius: var(--radius);
		padding: 1.75rem;
		width: min(440px, 90vw);
		box-shadow: var(--shadow);
		background: var(--color-paper);
	}

	dialog::backdrop {
		background: rgba(22, 16, 11, 0.4);
	}

	dialog h2 {
		font-size: 22px;
		line-height: 1.2;
	}

	.delete-copy {
		font-size: 13px;
		color: var(--color-muted);
		line-height: 1.55;
		margin-top: 9px;
	}

	dialog .rule {
		margin: 17px 0;
	}

	.dialog-actions {
		display: flex;
		justify-content: flex-end;
		gap: 9px;
	}

	@media (max-width: 720px) {
		.detail-layout {
			flex-direction: column;
			gap: 24px;
		}

		.cover-section {
			width: 160px;
		}

		.titleblock h1 {
			font-size: 30px;
		}

		.original-title {
			font-size: 18px;
		}

		.info-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
