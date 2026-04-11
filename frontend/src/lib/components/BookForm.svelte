<script lang="ts">
	import type { BookCreate, BookStatus } from '$lib/types';

	let { initial = {}, submitLabel = 'Save', onSubmit, onCancel }: {
		initial?: Partial<BookCreate>;
		submitLabel?: string;
		onSubmit: (data: BookCreate) => void;
		onCancel?: () => void;
	} = $props();

	let title = $state(initial.title ?? '');
	let original_title = $state(initial.original_title ?? '');
	let author = $state(initial.author ?? '');
	let publisher = $state(initial.publisher ?? '');
	let original_pub_date = $state(initial.original_pub_date ?? '');
	let publishing_date = $state(initial.publishing_date ?? '');
	let edition_date = $state(initial.edition_date ?? '');
	let language = $state(initial.language ?? '');
	let original_language = $state(initial.original_language ?? '');
	let status: BookStatus = $state(initial.status ?? 'available');
	let notes = $state(initial.notes ?? '');

	function handleSubmit(e: Event) {
		e.preventDefault();
		onSubmit({
			title,
			original_title: original_title || null,
			author,
			publisher: publisher || null,
			original_pub_date: original_pub_date || null,
			publishing_date: publishing_date || null,
			edition_date: edition_date || null,
			language: language || null,
			original_language: original_language || null,
			status,
			notes: notes || null
		});
	}
</script>

<form onsubmit={handleSubmit} class="book-form">
	<div class="form-row">
		<div class="field">
			<label for="title">Title *</label>
			<input id="title" type="text" bind:value={title} required />
		</div>
		<div class="field">
			<label for="original_title">Original Title</label>
			<input id="original_title" type="text" bind:value={original_title} />
		</div>
	</div>

	<div class="form-row">
		<div class="field">
			<label for="author">Author *</label>
			<input id="author" type="text" bind:value={author} required />
		</div>
		<div class="field">
			<label for="publisher">Publisher</label>
			<input id="publisher" type="text" bind:value={publisher} />
		</div>
	</div>

	<div class="form-row triple">
		<div class="field">
			<label for="original_pub_date">Original Publication</label>
			<input id="original_pub_date" type="text" bind:value={original_pub_date} placeholder="e.g. 1605" />
		</div>
		<div class="field">
			<label for="publishing_date">Publishing Date</label>
			<input id="publishing_date" type="text" bind:value={publishing_date} placeholder="e.g. 2020" />
		</div>
		<div class="field">
			<label for="edition_date">Edition Date</label>
			<input id="edition_date" type="text" bind:value={edition_date} placeholder="e.g. 2023-05" />
		</div>
	</div>

	<div class="form-row triple">
		<div class="field">
			<label for="language">Language</label>
			<input id="language" type="text" bind:value={language} placeholder="e.g. Spanish" />
		</div>
		<div class="field">
			<label for="original_language">Original Language</label>
			<input id="original_language" type="text" bind:value={original_language} placeholder="e.g. English" />
		</div>
		<div class="field">
			<label for="status">Status</label>
			<select id="status" bind:value={status}>
				<option value="available">Available</option>
				<option value="borrowed">Borrowed</option>
				<option value="archived">Archived</option>
			</select>
		</div>
	</div>

	<div class="field">
		<label for="notes">Notes</label>
		<textarea id="notes" bind:value={notes} placeholder="Optional notes about this book..."></textarea>
	</div>

	<div class="form-actions">
		{#if onCancel}
			<button type="button" onclick={onCancel}>Cancel</button>
		{/if}
		<button type="submit" class="primary">{submitLabel}</button>
	</div>
</form>

<style>
	.book-form {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1rem;
	}

	.form-row.triple {
		grid-template-columns: 1fr 1fr 1fr;
	}

	.field {
		display: flex;
		flex-direction: column;
	}

	.form-actions {
		display: flex;
		gap: 0.75rem;
		justify-content: flex-end;
		padding-top: 0.5rem;
	}

	@media (max-width: 640px) {
		.form-row, .form-row.triple {
			grid-template-columns: 1fr;
		}
	}
</style>
