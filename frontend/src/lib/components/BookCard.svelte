<script lang="ts">
	import type { Book } from '$lib/types';

	let { book, showActions = false, onAction }: {
		book: Book;
		showActions?: boolean;
		onAction?: (action: string, book: Book) => void;
	} = $props();

	const coverUrl = $derived(
		book.cover_image_path ? `/uploads/${book.cover_image_path}` : null
	);
</script>

<a href="/books/{book.id}" class="card">
	<div class="cover">
		{#if coverUrl}
			<img src={coverUrl} alt="{book.title} cover" />
		{:else}
			<div class="placeholder">
				<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>
			</div>
		{/if}
	</div>
	<div class="info">
		<h3 class="title">{book.title}</h3>
		<p class="author">{book.author}</p>
		<span class="badge {book.status}">{book.status}</span>
		{#if book.status === 'borrowed' && book.borrower_name}
			<p class="borrower">→ {book.borrower_name}</p>
		{/if}
	</div>
	{#if showActions && onAction}
		<div class="actions">
			{#if book.status === 'available'}
				<button class="small" onclick={(e) => { e.preventDefault(); onAction('borrow', book); }}>Borrow</button>
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
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		overflow: hidden;
		text-decoration: none;
		color: inherit;
		transition: box-shadow 0.15s ease;
	}

	.card:hover {
		box-shadow: var(--shadow);
		text-decoration: none;
	}

	.cover {
		aspect-ratio: 2 / 3;
		overflow: hidden;
		background: #f3f4f6;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.cover img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.placeholder {
		color: #d1d5db;
	}

	.info {
		padding: 0.75rem;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.title {
		font-size: 0.875rem;
		font-weight: 600;
		line-height: 1.3;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}

	.author {
		font-size: 0.8rem;
		color: var(--color-text-secondary);
	}

	.borrower {
		font-size: 0.75rem;
		color: var(--color-warning);
		font-style: italic;
		margin-top: 0.1rem;
	}

	.actions {
		padding: 0 0.75rem 0.75rem;
	}
</style>
