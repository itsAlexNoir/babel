<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { Book } from '$lib/types';
	import BookList from '$lib/components/BookList.svelte';
	import SearchBar from '$lib/components/SearchBar.svelte';

	let books: Book[] = $state([]);
	let loading = $state(true);
	let search = $state('');

	async function load() {
		loading = true;
		try {
			books = await api.books.list({ status: 'available', search: search || undefined });
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
</script>

<div class="page-header">
	<h1>Catalogue</h1>
	<a href="/books/new"><button class="primary">+ Add Book</button></a>
</div>

<div class="search-wrapper">
	<SearchBar value={search} onSearch={handleSearch} />
</div>

{#if loading}
	<p class="loading">Loading...</p>
{:else}
	<BookList {books} emptyMessage="No books in the catalogue yet. Add one to get started!" />
{/if}

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

	.search-wrapper {
		margin-bottom: 1.5rem;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: var(--color-text-secondary);
	}
</style>
