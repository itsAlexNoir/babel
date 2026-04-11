<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { Book } from '$lib/types';
	import BookList from '$lib/components/BookList.svelte';
	import SearchBar from '$lib/components/SearchBar.svelte';
	import { toast } from '$lib/toast';

	let books: Book[] = $state([]);
	let loading = $state(true);
	let search = $state('');

	async function load() {
		loading = true;
		try {
			books = await api.archived.list(search || undefined);
		} catch {
			books = [];
		}
		loading = false;
	}

	onMount(load);

	function handleSearch(query: string) {
		search = query;
		load();
	}

	async function handleAction(action: string, book: Book) {
		if (action === 'restore') {
			try {
				await api.books.updateStatus(book.id, 'available');
				toast(`"${book.title}" restored.`, 'success');
				load();
			} catch {
				toast('Failed to restore book.', 'error');
			}
		}
	}
</script>

<div class="page-header">
	<h1>Archived Books</h1>
</div>

<div class="search-wrapper">
	<SearchBar value={search} onSearch={handleSearch} />
</div>

{#if loading}
	<p class="loading">Loading...</p>
{:else}
	<BookList {books} emptyMessage="No archived books." showActions onAction={handleAction} />
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
