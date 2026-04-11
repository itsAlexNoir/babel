<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { BookStats } from '$lib/types';

	let stats: BookStats | null = $state(null);

	onMount(async () => {
		try {
			stats = await api.books.stats();
		} catch {
			// API might not be running yet
		}
	});
</script>

<div class="home">
	<h1>📚 Babel</h1>
	<p class="subtitle">Library Catalogue Manager</p>

	{#if stats}
		<div class="stats">
			<a href="/books" class="stat-card">
				<span class="stat-number">{stats.total}</span>
				<span class="stat-label">Total Books</span>
			</a>
			<a href="/books" class="stat-card">
				<span class="stat-number">{stats.available}</span>
				<span class="stat-label">Available</span>
			</a>
			<a href="/borrowed" class="stat-card">
				<span class="stat-number">{stats.borrowed}</span>
				<span class="stat-label">Borrowed</span>
			</a>
			<a href="/archived" class="stat-card">
				<span class="stat-number">{stats.archived}</span>
				<span class="stat-label">Archived</span>
			</a>
		</div>
	{/if}

	<div class="actions">
		<a href="/books/new"><button class="primary">Add a Book</button></a>
		<a href="/scan"><button>Scan a Book</button></a>
	</div>
</div>

<style>
	.home {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 4rem 2rem;
		text-align: center;
	}

	h1 {
		font-size: 2.5rem;
		font-weight: 600;
	}

	.subtitle {
		color: var(--color-text-secondary);
		margin-top: 0.5rem;
		font-size: 1.1rem;
	}

	.stats {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1rem;
		margin-top: 2.5rem;
		width: 100%;
		max-width: 600px;
	}

	.stat-card {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1.25rem;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		text-decoration: none;
		color: inherit;
		transition: box-shadow 0.15s ease;
	}

	.stat-card:hover {
		box-shadow: var(--shadow);
		text-decoration: none;
	}

	.stat-number {
		font-size: 1.75rem;
		font-weight: 600;
	}

	.stat-label {
		font-size: 0.8rem;
		color: var(--color-text-secondary);
	}

	.actions {
		display: flex;
		gap: 0.75rem;
		margin-top: 2rem;
	}

	@media (max-width: 640px) {
		.stats {
			grid-template-columns: repeat(2, 1fr);
		}
	}
</style>
