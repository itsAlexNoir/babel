<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { replaceState } from '$app/navigation';
	import { api } from '$lib/api';
	import type { Book } from '$lib/types';
	import BookList from '$lib/components/BookList.svelte';
	import BorrowDialog from '$lib/components/BorrowDialog.svelte';
	import SearchBar from '$lib/components/SearchBar.svelte';
	import { toast } from '$lib/toast';

	let books: Book[] = $state([]);
	let loading = $state(true);
	let search = $state(page.url.searchParams.get('search') ?? '');
	let viewMode = $state<'grid' | 'list'>('grid');
	let borrowingBook = $state<Book | null>(null);

	async function load() {
		loading = true;
		try {
			books = await api.books.list({ status: 'available', search: search || undefined });
		} catch {
			books = [];
		}
		loading = false;
	}

	onMount(() => {
		const saved = localStorage.getItem('books-view-mode');
		if (saved === 'list' || saved === 'grid') viewMode = saved;
		load();
	});

	function handleSearch(query: string) {
		search = query;
		const url = new URL(page.url);
		if (query) {
			url.searchParams.set('search', query);
		} else {
			url.searchParams.delete('search');
		}
		replaceState(url, {});
		load();
	}

	function setViewMode(mode: 'grid' | 'list') {
		viewMode = mode;
		localStorage.setItem('books-view-mode', mode);
	}

	function handleAction(action: string, book: Book) {
		if (action === 'borrow') {
			borrowingBook = book;
		}
	}

	async function handleBorrowConfirm(borrowerName: string) {
		if (!borrowingBook) return;
		try {
			await api.books.borrow(borrowingBook.id, borrowerName);
			toast(`"${borrowingBook.title}" lent to ${borrowerName}.`, 'success');
			borrowingBook = null;
			load();
		} catch {
			toast('Failed to mark as borrowed.', 'error');
		}
	}
</script>

<div class="page-header">
	<h1>Catalogue</h1>
	<div class="header-actions">
		<div class="view-toggle">
			<button
				class="toggle-btn"
				class:active={viewMode === 'grid'}
				title="Grid view"
				onclick={() => setViewMode('grid')}
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
			</button>
			<button
				class="toggle-btn"
				class:active={viewMode === 'list'}
				title="List view"
				onclick={() => setViewMode('list')}
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
			</button>
		</div>
		<a href="/books/new"><button class="primary">+ Add Book</button></a>
	</div>
</div>

<div class="search-wrapper">
	<SearchBar value={search} onSearch={handleSearch} />
</div>

{#if loading}
	<p class="loading">Loading...</p>
{:else}
	<BookList {books} {viewMode} emptyMessage="No books in the catalogue yet. Add one to get started!" showActions onAction={handleAction} />
{/if}

<BorrowDialog
	book={borrowingBook}
	onConfirm={handleBorrowConfirm}
	onClose={() => borrowingBook = null}
/>

<style>
	.page-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 1.5rem;
	}

	h1 {
		font-size: 1.5rem;
		font-weight: 600;
	}

	.header-actions {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.view-toggle {
		display: flex;
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		overflow: hidden;
	}

	.toggle-btn {
		padding: 0.4rem 0.6rem;
		border: none;
		border-radius: 0;
		background: var(--color-surface);
		color: var(--color-text-secondary);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.toggle-btn:hover {
		background: var(--color-bg);
		color: var(--color-text);
	}

	.toggle-btn.active {
		background: var(--color-primary);
		color: white;
	}

	.toggle-btn + .toggle-btn {
		border-left: 1px solid var(--color-border);
	}

	.search-wrapper {
		margin-bottom: 1.5rem;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: var(--color-text-secondary);
	}
</style>
