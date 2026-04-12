<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { LibraryStats } from '$lib/types';

	let stats: LibraryStats | null = $state(null);
	let loading = $state(true);

	onMount(async () => {
		try {
			stats = await api.books.libraryStats();
		} catch {
			stats = null;
		}
		loading = false;
	});

	function barWidth(count: number, max: number): string {
		return `${Math.max((count / max) * 100, 2)}%`;
	}
</script>

<div class="page-header">
	<h1>Library Statistics</h1>
</div>

{#if loading}
	<p class="loading">Loading...</p>
{:else if stats}
	<div class="overview">
		<div class="stat-card">
			<span class="stat-number">{stats.total}</span>
			<span class="stat-label">Total Books</span>
		</div>
		<div class="stat-card available">
			<span class="stat-number">{stats.available}</span>
			<span class="stat-label">Available</span>
		</div>
		<div class="stat-card borrowed">
			<span class="stat-number">{stats.borrowed}</span>
			<span class="stat-label">Borrowed</span>
		</div>
		<div class="stat-card archived">
			<span class="stat-number">{stats.archived}</span>
			<span class="stat-label">Archived</span>
		</div>
	</div>

	<div class="charts-grid">
		<!-- Top Authors -->
		<section class="chart-card">
			<h2>Top Authors</h2>
			<div class="bar-chart">
				{#each stats.top_authors as item}
					{@const max = stats.top_authors[0]?.count ?? 1}
					<div class="bar-row">
						<span class="bar-label" title={item.name}>{item.name}</span>
						<div class="bar-track">
							<div class="bar-fill author" style="width: {barWidth(item.count, max)}"></div>
						</div>
						<span class="bar-count">{item.count}</span>
					</div>
				{/each}
			</div>
		</section>

		<!-- Top Publishers -->
		<section class="chart-card">
			<h2>Top Publishers</h2>
			<div class="bar-chart">
				{#each stats.top_publishers as item}
					{@const max = stats.top_publishers[0]?.count ?? 1}
					<div class="bar-row">
						<span class="bar-label" title={item.name}>{item.name}</span>
						<div class="bar-track">
							<div class="bar-fill publisher" style="width: {barWidth(item.count, max)}"></div>
						</div>
						<span class="bar-count">{item.count}</span>
					</div>
				{/each}
			</div>
		</section>

		<!-- Languages -->
		<section class="chart-card">
			<h2>Languages</h2>
			<div class="bar-chart">
				{#each stats.languages as item}
					{@const max = stats.languages[0]?.count ?? 1}
					<div class="bar-row">
						<span class="bar-label" title={item.name}>{item.name}</span>
						<div class="bar-track">
							<div class="bar-fill language" style="width: {barWidth(item.count, max)}"></div>
						</div>
						<span class="bar-count">{item.count}</span>
					</div>
				{/each}
			</div>
		</section>

		<!-- Books by Decade -->
		<section class="chart-card">
			<h2>Books by Decade</h2>
			<div class="bar-chart">
				{#each stats.books_by_decade as item}
					{@const max = Math.max(...stats.books_by_decade.map(d => d.count))}
					<div class="bar-row">
						<span class="bar-label">{item.name}</span>
						<div class="bar-track">
							<div class="bar-fill decade" style="width: {barWidth(item.count, max)}"></div>
						</div>
						<span class="bar-count">{item.count}</span>
					</div>
				{/each}
			</div>
		</section>
	</div>
{:else}
	<p class="loading">Failed to load statistics.</p>
{/if}

<style>
	.page-header {
		margin-bottom: 1.5rem;
	}

	h1 {
		font-size: 1.5rem;
		font-weight: 600;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: var(--color-text-secondary);
	}

	/* Overview cards */
	.overview {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1rem;
		margin-bottom: 2rem;
	}

	.stat-card {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1.25rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.25rem;
	}

	.stat-number {
		font-size: 2rem;
		font-weight: 600;
		line-height: 1;
	}

	.stat-label {
		font-size: 0.8rem;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
	}

	.stat-card.available .stat-number { color: var(--color-success); }
	.stat-card.borrowed .stat-number { color: var(--color-warning); }
	.stat-card.archived .stat-number { color: var(--color-text-secondary); }

	/* Charts grid */
	.charts-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1.5rem;
	}

	.chart-card {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1.25rem;
	}

	.chart-card h2 {
		font-size: 0.95rem;
		font-weight: 600;
		margin-bottom: 1rem;
	}

	/* Bar chart */
	.bar-chart {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}

	.bar-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.bar-label {
		width: 140px;
		min-width: 140px;
		font-size: 0.8rem;
		color: var(--color-text);
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.bar-track {
		flex: 1;
		height: 18px;
		background: var(--color-bg);
		border-radius: 3px;
		overflow: hidden;
	}

	.bar-fill {
		height: 100%;
		border-radius: 3px;
		transition: width 0.4s ease;
	}

	.bar-fill.author { background: var(--color-primary); }
	.bar-fill.publisher { background: var(--color-success); }
	.bar-fill.language { background: var(--color-warning); }
	.bar-fill.decade { background: #8b5cf6; }

	.bar-count {
		width: 32px;
		text-align: right;
		font-size: 0.8rem;
		font-weight: 500;
		color: var(--color-text-secondary);
	}

	/* Responsive */
	@media (max-width: 900px) {
		.overview {
			grid-template-columns: repeat(2, 1fr);
		}
		.charts-grid {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 480px) {
		.overview {
			grid-template-columns: 1fr;
		}
	}
</style>
