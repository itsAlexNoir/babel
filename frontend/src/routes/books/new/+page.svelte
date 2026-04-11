<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import type { BookCreate } from '$lib/types';
	import BookForm from '$lib/components/BookForm.svelte';
	import { toast } from '$lib/toast';

	let saving = $state(false);

	async function handleSubmit(data: BookCreate) {
		saving = true;
		try {
			const book = await api.books.create(data);
			toast('Book added successfully!', 'success');
			goto(`/books/${book.id}`);
		} catch (err) {
			toast('Failed to add book.', 'error');
		}
		saving = false;
	}
</script>

<div class="page-header">
	<h1>Add New Book</h1>
</div>

<div class="form-container">
	<BookForm submitLabel={saving ? 'Saving...' : 'Add Book'} onSubmit={handleSubmit} onCancel={() => history.back()} />
</div>

<style>
	.page-header {
		margin-bottom: 1.5rem;
	}

	h1 {
		font-size: 1.5rem;
		font-weight: 600;
	}

	.form-container {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1.5rem;
		max-width: 800px;
	}
</style>
