<script lang="ts">
	import type { Book } from '$lib/types';
	import BookCover from './BookCover.svelte';

	let { book, showActions = false, onAction }: {
		book: Book;
		showActions?: boolean;
		onAction?: (action: string, book: Book) => void;
	} = $props();

	const year = $derived(book.publishing_date ?? book.original_pub_date ?? book.edition_date ?? null);
</script>

<a href="/books/{book.id}" class="card">
	<BookCover {book} size="m" />
	<div class="info">
		<h3 class="title">{book.title}</h3>
		<p class="author">{book.author}</p>
		{#if book.status === 'borrowed'}
			<span class="stat out"><span class="dot"></span>{book.borrower_name}</span>
		{:else if book.status === 'archived'}
			<span class="stat arch">Archived</span>
		{:else}
			<span class="meta mono">{book.publisher ?? '—'}{#if year} · {year}{/if}</span>
		{/if}
	</div>
	{#if showActions && onAction}
		<div class="actions">
			{#if book.status === 'available'}
				<button class="small" onclick={(e) => { e.preventDefault(); onAction('borrow', book); }}>Lend</button>
			{:else if book.status === 'borrowed'}
				<button class="small" onclick={(e) => { e.preventDefault(); onAction('return', book); }}>Return</button>
			{:else if book.status === 'archived'}
				<button class="small" onclick={(e) => { e.preventDefault(); onAction('restore', book); }}>Restore</button>
			{/if}
		</div>
	{/if}
</a>

<style>
	.card {
		display: flex;
		flex-direction: column;
		gap: 9px;
		text-decoration: none;
		color: inherit;
	}

	.card:hover {
		text-decoration: none;
	}

	.card:hover .title {
		color: var(--color-spot);
	}

	.info {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.title {
		font-family: var(--font-serif);
		font-size: 16px;
		font-weight: 400;
		line-height: 1.22;
		color: var(--color-ink);
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
		transition: color 0.12s ease;
	}

	.author {
		font-size: 11.5px;
		color: var(--color-muted);
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.meta {
		font-size: 10px;
		color: var(--color-faint);
		margin-top: 1px;
	}

	.actions {
		margin-top: -2px;
	}
</style>
