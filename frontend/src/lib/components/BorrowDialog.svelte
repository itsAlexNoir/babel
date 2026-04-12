<script lang="ts">
	import type { Book } from '$lib/types';

	let { book, onConfirm, onClose }: {
		book: Book | null;
		onConfirm: (borrowerName: string) => void;
		onClose: () => void;
	} = $props();

	let borrowerName = $state('');
	let dialogEl: HTMLDialogElement | undefined = $state();

	$effect(() => {
		if (book && dialogEl) {
			borrowerName = '';
			dialogEl.showModal();
		} else if (!book && dialogEl) {
			dialogEl.close();
		}
	});

	function submit(e: Event) {
		e.preventDefault();
		if (borrowerName.trim()) {
			onConfirm(borrowerName.trim());
		}
	}
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<dialog
	bind:this={dialogEl}
	onclose={onClose}
	onclick={(e) => { if (e.target === dialogEl) onClose(); }}
>
	{#if book}
		<form onsubmit={submit}>
			<h2>Lend book</h2>
			<p class="book-title">"{book.title}"</p>
			<label for="borrower">Borrower's name</label>
			<input
				id="borrower"
				type="text"
				bind:value={borrowerName}
				placeholder="Enter name..."
				required
				autofocus
			/>
			<div class="actions">
				<button type="button" onclick={onClose}>Cancel</button>
				<button type="submit" class="primary" disabled={!borrowerName.trim()}>Confirm</button>
			</div>
		</form>
	{/if}
</dialog>

<style>
	dialog {
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1.5rem;
		width: min(420px, 90vw);
		box-shadow: 0 8px 24px rgba(0,0,0,0.12);
		background: var(--color-surface);
	}

	dialog::backdrop {
		background: rgba(0, 0, 0, 0.35);
	}

	h2 {
		font-size: 1.1rem;
		font-weight: 600;
		margin-bottom: 0.25rem;
	}

	.book-title {
		font-size: 0.875rem;
		color: var(--color-text-secondary);
		margin-bottom: 1rem;
		font-style: italic;
	}

	label {
		display: block;
		font-size: 0.8rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
		margin-bottom: 0.4rem;
	}

	input {
		width: 100%;
		font-family: inherit;
		font-size: 0.875rem;
		padding: 0.5rem 0.75rem;
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		outline: none;
		box-sizing: border-box;
	}

	input:focus {
		border-color: var(--color-primary);
	}

	.actions {
		display: flex;
		justify-content: flex-end;
		gap: 0.5rem;
		margin-top: 1rem;
	}
</style>
