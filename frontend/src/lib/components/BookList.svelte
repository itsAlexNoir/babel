<script lang="ts">
	import type { Book } from '$lib/types';
	import BookCard from './BookCard.svelte';

	let { books, emptyMessage = 'No books found.', showActions = false, onAction }: {
		books: Book[];
		emptyMessage?: string;
		showActions?: boolean;
		onAction?: (action: string, book: Book) => void;
	} = $props();
</script>

{#if books.length === 0}
	<div class="empty">
		<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>
		<p>{emptyMessage}</p>
	</div>
{:else}
	<div class="grid">
		{#each books as book (book.id)}
			<BookCard {book} {showActions} {onAction} />
		{/each}
	</div>
{/if}

<style>
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
		gap: 1.25rem;
	}

	.empty {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		padding: 4rem 2rem;
		color: var(--color-text-secondary);
	}

	.empty p {
		font-size: 0.9rem;
	}
</style>
