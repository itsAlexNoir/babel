<script lang="ts">
	import type { Book } from '$lib/types';
	import BookCard from './BookCard.svelte';

	type SortKey = 'title' | 'author' | 'publisher' | 'year' | 'added';
	type SortDir = 'asc' | 'desc';

	let { books, emptyMessage = 'No books found.', showActions = false, onAction, viewMode = 'grid' }: {
		books: Book[];
		emptyMessage?: string;
		showActions?: boolean;
		onAction?: (action: string, book: Book) => void;
		viewMode?: 'grid' | 'list';
	} = $props();

	let sortKey = $state<SortKey>('added');
	let sortDir = $state<SortDir>('desc');

	const SORT_LABELS: Record<SortKey, string> = {
		title: 'Title',
		author: 'Author',
		publisher: 'Publisher',
		year: 'Year',
		added: 'Recently Added',
	};

	function toggleSort(key: SortKey) {
		if (sortKey === key) {
			sortDir = sortDir === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDir = key === 'added' ? 'desc' : 'asc';
		}
	}

	function bookYear(book: Book): number {
		const y = book.publishing_date ?? book.original_pub_date ?? book.edition_date;
		return y ? parseInt(y.slice(0, 4)) || 0 : 0;
	}

	const sortedBooks = $derived.by(() => {
		return [...books].sort((a, b) => {
			let cmp = 0;
			if (sortKey === 'title') {
				cmp = a.title.localeCompare(b.title);
			} else if (sortKey === 'author') {
				cmp = a.author.localeCompare(b.author);
			} else if (sortKey === 'publisher') {
				cmp = (a.publisher ?? '').localeCompare(b.publisher ?? '');
			} else if (sortKey === 'year') {
				cmp = bookYear(a) - bookYear(b);
			} else if (sortKey === 'added') {
				cmp = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
			}
			return sortDir === 'asc' ? cmp : -cmp;
		});
	});

	const coverUrl = (book: Book) =>
		book.cover_image_path ? `/uploads/${book.cover_image_path}` : null;

	const year = (book: Book) =>
		book.publishing_date ?? book.original_pub_date ?? book.edition_date ?? null;
</script>

{#if books.length === 0}
	<div class="empty">
		<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>
		<p>{emptyMessage}</p>
	</div>
{:else if viewMode === 'grid'}
	<div class="sort-bar">
		<span class="sort-label">Sort:</span>
		{#each Object.entries(SORT_LABELS) as [key, label]}
			<button
				class="sort-btn"
				class:active={sortKey === key}
				onclick={() => toggleSort(key as SortKey)}
			>
				{label}
				{#if sortKey === key}
					<span class="sort-arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>
				{/if}
			</button>
		{/each}
	</div>
	<div class="grid">
		{#each sortedBooks as book (book.id)}
			<BookCard {book} {showActions} {onAction} />
		{/each}
	</div>
{:else}
	<div class="list-container">
		<table class="list-table">
			<thead>
				<tr>
					<th class="col-cover"></th>
					<th class="col-title">
						<button class="col-sort-btn" class:active={sortKey === 'title'} onclick={() => toggleSort('title')}>
							Title {#if sortKey === 'title'}<span class="sort-arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>{/if}
						</button>
					</th>
					<th class="col-author">
						<button class="col-sort-btn" class:active={sortKey === 'author'} onclick={() => toggleSort('author')}>
							Author {#if sortKey === 'author'}<span class="sort-arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>{/if}
						</button>
					</th>
					<th class="col-publisher">
						<button class="col-sort-btn" class:active={sortKey === 'publisher'} onclick={() => toggleSort('publisher')}>
							Publisher {#if sortKey === 'publisher'}<span class="sort-arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>{/if}
						</button>
					</th>
					<th class="col-year">
						<button class="col-sort-btn" class:active={sortKey === 'year'} onclick={() => toggleSort('year')}>
							Year {#if sortKey === 'year'}<span class="sort-arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>{/if}
						</button>
					</th>
					<th class="col-language">Language</th>
					<th class="col-borrower">Borrower</th>
					<th class="col-added">Added</th>
					<th class="col-status">Status</th>
					{#if showActions}
						<th class="col-actions"></th>
					{/if}
				</tr>
			</thead>
			<tbody>
				{#each sortedBooks as book (book.id)}
					<tr class="list-row" onclick={() => window.location.href = `/books/${book.id}`}>
						<td class="col-cover">
							<div class="thumb">
								{#if coverUrl(book)}
									<img src={coverUrl(book)} alt="{book.title} cover" />
								{:else}
									<div class="thumb-placeholder">
										<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>
									</div>
								{/if}
							</div>
						</td>
						<td class="col-title">
							<a href="/books/{book.id}" class="title-link">{book.title}</a>
							{#if book.original_title}
								<span class="original-title">{book.original_title}</span>
							{/if}
							{#if book.tags}
								<div class="row-tags">
									{#each book.tags.split(';') as tag}
										<span class="row-tag">{tag.trim()}</span>
									{/each}
								</div>
							{/if}
						</td>
						<td class="col-author">
							{book.author}
							{#if book.translator}
								<span class="original-title">tr. {book.translator}</span>
							{/if}
						</td>
					<td class="col-publisher">{book.publisher ?? '—'}</td>
					<td class="col-year">{year(book) ?? '—'}</td>
					<td class="col-language">{book.language ?? '—'}</td>
					<td class="col-borrower">
						{#if book.borrower_name}
							<span class="borrower-name">{book.borrower_name}</span>
							{#if book.borrowed_at}
								<span class="original-title">{new Date(book.borrowed_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}</span>
							{/if}
						{:else if book.archived_at}
							<span class="original-title">archived {new Date(book.archived_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}</span>
						{:else}
							—
						{/if}
					</td>
					<td class="col-added">{new Date(book.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}</td>
					<td class="col-status">
						<span class="badge {book.status}">{book.status}</span>
					</td>
					{#if showActions && onAction}
						<td class="col-actions" onclick={(e) => e.stopPropagation()}>
							{#if book.status === 'available'}
								<button class="small" onclick={() => onAction('borrow', book)}>Borrow</button>
							{:else if book.status === 'borrowed'}
								<button class="small" onclick={() => onAction('return', book)}>Return</button>
							{:else if book.status === 'archived'}
								<button class="small" onclick={() => onAction('restore', book)}>Restore</button>
							{/if}
						</td>
					{/if}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

<style>
	/* Sort bar (grid view) */
	.sort-bar {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		margin-bottom: 1rem;
		flex-wrap: wrap;
	}

	.sort-label {
		font-size: 0.8rem;
		color: var(--color-text-secondary);
		margin-right: 0.25rem;
	}

	.sort-btn {
		font-size: 0.8rem;
		padding: 0.25rem 0.6rem;
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		background: var(--color-surface);
		color: var(--color-text-secondary);
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		gap: 0.2rem;
	}

	.sort-btn:hover {
		background: var(--color-bg);
		color: var(--color-text);
	}

	.sort-btn.active {
		background: var(--color-primary);
		border-color: var(--color-primary);
		color: white;
	}

	.sort-arrow {
		font-size: 0.75rem;
	}

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

	/* List view */
	.list-container {
		overflow-x: auto;
	}

	.list-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.875rem;
	}

	.list-table thead th {
		text-align: left;
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: var(--color-text-secondary);
		padding: 0 0;
		border-bottom: 1px solid var(--color-border);
		white-space: nowrap;
	}

	/* Sortable column header buttons */
	.col-sort-btn {
		all: unset;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		padding: 0.5rem 0.75rem;
		width: 100%;
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: var(--color-text-secondary);
		white-space: nowrap;
		border-radius: 4px;
	}

	.col-sort-btn:hover {
		color: var(--color-text);
		background: var(--color-bg);
	}

	.col-sort-btn.active {
		color: var(--color-primary);
	}

	.list-row {
		cursor: pointer;
		transition: background 0.1s ease;
	}

	.list-row:hover {
		background: var(--color-bg);
	}

	.list-row td {
		padding: 0.6rem 0.75rem;
		border-bottom: 1px solid var(--color-border);
		vertical-align: middle;
	}

	.thumb {
		width: 32px;
		height: 48px;
		border-radius: 3px;
		overflow: hidden;
		flex-shrink: 0;
	}

	.thumb img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.thumb-placeholder {
		width: 100%;
		height: 100%;
		background: #f3f4f6;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #d1d5db;
	}

	.title-link {
		font-weight: 600;
		color: var(--color-text);
		text-decoration: none;
		display: block;
	}

	.title-link:hover {
		color: var(--color-primary);
		text-decoration: none;
	}

	.original-title {
		display: block;
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		font-style: italic;
		margin-top: 1px;
	}

	.row-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
		margin-top: 0.25rem;
	}

	.row-tag {
		font-size: 0.7rem;
		padding: 0.1rem 0.45rem;
		background: var(--color-bg);
		border: 1px solid var(--color-border);
		border-radius: 999px;
		color: var(--color-text-secondary);
		white-space: nowrap;
	}

	.col-cover { width: 44px; }
	.col-title { min-width: 180px; }
	.col-author { min-width: 130px; white-space: nowrap; }
	.col-publisher { min-width: 120px; color: var(--color-text-secondary); }
	.col-year { width: 60px; color: var(--color-text-secondary); white-space: nowrap; }
	.col-language { width: 90px; color: var(--color-text-secondary); }
	.col-borrower { min-width: 120px; }
	.borrower-name { font-weight: 500; color: var(--color-warning); display: block; }
	.col-added { width: 100px; color: var(--color-text-secondary); white-space: nowrap; font-size: 0.8rem; }
	.col-status { width: 100px; }
	.col-actions { width: 80px; }
</style>
