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
	<p class="eyebrow">Library catalogue</p>
	<h1>A record of every book<br />that has passed through here.</h1>

	{#if stats}
		<div class="stats">
			<a href="/books" class="stat">
				<span class="num">{stats.total}</span>
				<span class="lbl">Total books</span>
			</a>
			<a href="/books?status=available" class="stat">
				<span class="num">{stats.available}</span>
				<span class="lbl">On shelf</span>
			</a>
			<a href="/books?status=borrowed" class="stat">
				<span class="num">{stats.borrowed}</span>
				<span class="lbl">On loan</span>
			</a>
			<a href="/books?status=archived" class="stat">
				<span class="num">{stats.archived}</span>
				<span class="lbl">Archived</span>
			</a>
		</div>
	{/if}

	<div class="actions">
		<a href="/books/new"><button class="primary">Add a book</button></a>
		<a href="/scan"><button>Scan a book</button></a>
	</div>
</div>

<style>
	.home {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		padding: 5rem 1rem 3rem;
	}

	h1 {
		font-size: 2.6rem;
		line-height: 1.15;
		max-width: 18ch;
		margin-top: 0.6rem;
	}

	.stats {
		display: flex;
		gap: 44px;
		margin-top: 3rem;
		padding-top: 1.75rem;
		border-top: 1.5px solid var(--color-ink);
	}

	.stat {
		display: flex;
		flex-direction: column;
		gap: 3px;
		text-decoration: none;
		color: inherit;
	}

	.stat:hover {
		text-decoration: none;
	}

	.stat:hover .num {
		color: var(--color-spot);
	}

	.num {
		font-family: var(--font-serif);
		font-size: 2.1rem;
		line-height: 1;
		color: var(--color-ink);
		transition: color 0.12s ease;
	}

	.lbl {
		font-size: 10px;
		font-weight: 600;
		letter-spacing: 0.09em;
		text-transform: uppercase;
		color: var(--color-faint);
	}

	.actions {
		display: flex;
		gap: 0.75rem;
		margin-top: 2.5rem;
	}

	@media (max-width: 560px) {
		.stats {
			gap: 26px;
			flex-wrap: wrap;
			justify-content: center;
		}
	}
</style>
