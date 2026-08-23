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
			<p class="book-title">{book.title}</p>
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
		width: min(420px, 90vw);
		box-shadow: var(--shadow);
		background: var(--color-paper);
	}

	dialog::backdrop {
		background: rgba(22, 16, 11, 0.4);
	}

	h2 {
		font-family: var(--font-serif);
		font-size: 1.5rem;
		margin-bottom: 0.3rem;
	}

	.book-title {
		font-family: var(--font-serif);
		font-style: italic;
		font-size: 1.05rem;
		color: var(--color-muted);
		margin-bottom: 1.25rem;
	}

	.actions {
		display: flex;
		justify-content: flex-end;
		gap: 0.5rem;
		margin-top: 1.25rem;
	}
</style>
