<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { replaceState } from '$app/navigation';
	import { api } from '$lib/api';
	import type { Book } from '$lib/types';
	import BookList from '$lib/components/BookList.svelte';
	import SearchBar from '$lib/components/SearchBar.svelte';
	import { toast } from '$lib/toast';

	let books: Book[] = $state([]);
	let loading = $state(true);
	let search = $state(page.url.searchParams.get('search') ?? '');

	async function load() {
		loading = true;
		try {
			books = await api.borrowed.list(search || undefined);
		} catch {
			books = [];
		}
		loading = false;
	}

	onMount(load);

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

	async function handleAction(action: string, book: Book) {
		if (action === 'return') {
			try {
				await api.books.updateStatus(book.id, 'available');
				toast(`"${book.title}" returned.`, 'success');
				load();
			} catch {
				toast('Failed to return book.', 'error');
			}
		}
	}
</script>

<div class="page-header">
	<h1>Borrowed Books</h1>
</div>

<div class="search-wrapper">
	<SearchBar value={search} onSearch={handleSearch} />
</div>

{#if loading}
	<p class="loading">Loading...</p>
{:else}
	<BookList {books} emptyMessage="No borrowed books." showActions onAction={handleAction} />
{/if}

<style>
	.page-header {
		margin-bottom: 1.5rem;
	}

	h1 {
		font-size: 1.5rem;
		font-weight: 600;
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
