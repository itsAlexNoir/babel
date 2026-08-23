<script lang="ts">
	import type { Book } from '$lib/types';
	import BookCard from './BookCard.svelte';
	import BookCover from './BookCover.svelte';

	type SortKey = 'title' | 'author' | 'publisher' | 'year' | 'added';
	type SortDir = 'asc' | 'desc';

	let {
		books,
		viewMode = 'grid',
		showActions = false,
		onAction,
		onTagClick,
		sortKey = $bindable('added'),
		sortDir = $bindable('desc'),
		page = $bindable(1),
		pageSize = 40,
		emptyTitle = 'No books found.',
		emptyBody = '',
		emptyActionLabel,
		onEmptyAction,
	}: {
		books: Book[];
		viewMode?: 'grid' | 'list';
		showActions?: boolean;
		onAction?: (action: string, book: Book) => void;
		onTagClick?: (tag: string) => void;
		sortKey?: SortKey;
		sortDir?: SortDir;
		page?: number;
		pageSize?: number;
		emptyTitle?: string;
		emptyBody?: string;
		emptyActionLabel?: string;
		onEmptyAction?: () => void;
	} = $props();

	const SORT_LABELS: Record<SortKey, string> = {
		title: 'Title',
		author: 'Author',
		publisher: 'Publisher',
		year: 'Year',
		added: 'Recently added',
	};
	const SORT_KEYS: SortKey[] = ['added', 'title', 'author', 'publisher', 'year'];

	function toggleSort(key: SortKey) {
		if (sortKey === key) {
			sortDir = sortDir === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDir = key === 'added' ? 'desc' : 'asc';
		}
		page = 1;
	}

	function bookYear(book: Book): number {
		const y = book.publishing_date ?? book.original_pub_date ?? book.edition_date;
		return y ? parseInt(y.slice(0, 4)) || 0 : 0;
	}

	function bookTags(book: Book): string[] {
		return book.tags ? book.tags.split(';').map((t) => t.trim()).filter(Boolean) : [];
	}

	const sortedBooks = $derived.by(() => {
		return [...books].sort((a, b) => {
			let cmp = 0;
			if (sortKey === 'title') cmp = a.title.localeCompare(b.title);
			else if (sortKey === 'author') cmp = a.author.localeCompare(b.author);
			else if (sortKey === 'publisher') cmp = (a.publisher ?? '').localeCompare(b.publisher ?? '');
			else if (sortKey === 'year') cmp = bookYear(a) - bookYear(b);
			else if (sortKey === 'added') cmp = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
			return sortDir === 'asc' ? cmp : -cmp;
		});
	});

	const pageCount = $derived(Math.max(1, Math.ceil(sortedBooks.length / pageSize)));
	const safePage = $derived(Math.min(Math.max(page, 1), pageCount));
	const pageBooks = $derived(sortedBooks.slice((safePage - 1) * pageSize, safePage * pageSize));
	const rangeStart = $derived(sortedBooks.length === 0 ? 0 : (safePage - 1) * pageSize + 1);
	const rangeEnd = $derived(Math.min(safePage * pageSize, sortedBooks.length));

	const year = (book: Book) => book.publishing_date ?? book.original_pub_date ?? book.edition_date ?? null;

	const COLS = '32px minmax(0,1.3fr) minmax(150px,1fr) 120px 56px 120px 76px';
</script>

{#if books.length === 0}
	<div class="empty">
		<h3>{emptyTitle}</h3>
		{#if emptyBody}<p>{emptyBody}</p>{/if}
		{#if emptyActionLabel && onEmptyAction}
			<button class="small" onclick={onEmptyAction}>{emptyActionLabel}</button>
		{/if}
	</div>
{:else}
	{#if viewMode === 'grid'}
		<div class="sort-row">
			<span class="eyebrow">Sort</span>
			{#each SORT_KEYS as key}
				<button class="sort-link" class:on={sortKey === key} onclick={() => toggleSort(key)}>
					{SORT_LABELS[key]}
					{#if sortKey === key}<span class="arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>{/if}
				</button>
			{/each}
		</div>
		<div class="grid">
			{#each pageBooks as book (book.id)}
				<BookCard {book} {showActions} {onAction} />
			{/each}
		</div>
	{:else}
		<div class="list">
			<div class="row head" style:grid-template-columns={COLS}>
				<span></span>
				<button class="col-sort" class:on={sortKey === 'title'} onclick={() => toggleSort('title')}>
					Title / Author {#if sortKey === 'title' || sortKey === 'author'}<span class="arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>{/if}
				</button>
				<span class="eyebrow">Tags</span>
				<button class="col-sort" class:on={sortKey === 'publisher'} onclick={() => toggleSort('publisher')}>
					Publisher {#if sortKey === 'publisher'}<span class="arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>{/if}
				</button>
				<button class="col-sort" class:on={sortKey === 'year'} onclick={() => toggleSort('year')}>
					Year {#if sortKey === 'year'}<span class="arrow">{sortDir === 'asc' ? '↑' : '↓'}</span>{/if}
				</button>
				<span class="eyebrow">Status</span>
				<span></span>
			</div>
			{#each pageBooks as book (book.id)}
				<div class="row" style:grid-template-columns={COLS}>
					<div class="col-cover"><BookCover {book} size="s" /></div>
					<a href="/books/{book.id}" class="row-link">
						<div class="row-title">{book.title}</div>
						<div class="row-author">
							{book.author}
							{#if book.original_title}<span class="dim"> · {book.original_title}</span>{/if}
						</div>
					</a>
					<div class="col-tags">
						{#each bookTags(book) as tag}
							{#if onTagClick}
								<button class="tag" onclick={() => onTagClick(tag)}>{tag}</button>
							{:else}
								<span class="tag">{tag}</span>
							{/if}
						{/each}
					</div>
					<span class="col-publisher">{book.publisher ?? '—'}</span>
					<span class="col-year mono">{year(book) ?? '—'}</span>
					<span class="col-status">
						{#if book.status === 'available'}
							<span class="stat avail"><span class="dot"></span>On shelf</span>
						{:else if book.status === 'borrowed'}
							<span class="stat out"><span class="dot"></span>{book.borrower_name}</span>
						{:else}
							<span class="stat arch">Archived</span>
						{/if}
					</span>
					<span class="col-actions">
						{#if showActions && onAction}
							{#if book.status === 'available'}
								<button class="small quiet" onclick={() => onAction('borrow', book)}>Lend</button>
							{:else if book.status === 'borrowed'}
								<button class="small quiet" onclick={() => onAction('return', book)}>Return</button>
							{:else}
								<button class="small quiet" onclick={() => onAction('restore', book)}>Restore</button>
							{/if}
						{/if}
					</span>
				</div>
			{/each}
		</div>
	{/if}

	<div class="pagination">
		<span class="range">Rows <span class="mono">{rangeStart}–{rangeEnd}</span> of <span class="mono">{sortedBooks.length}</span></span>
		<div class="pager">
			<button class="quiet-btn" disabled={safePage <= 1} onclick={() => (page = safePage - 1)}>← Previous</button>
			<span class="mono page-indicator">{safePage} / {pageCount}</span>
			<button class="quiet-btn" disabled={safePage >= pageCount} onclick={() => (page = safePage + 1)}>Next →</button>
		</div>
	</div>
{/if}

<style>
	.empty {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		gap: 9px;
		padding: 4rem 1rem;
		border-top: 1px solid var(--color-ink);
		border-bottom: 1px solid var(--color-rule-faint);
	}

	.empty h3 {
		font-size: 20px;
	}

	.empty p {
		font-size: 12px;
		color: var(--color-muted);
		max-width: 34ch;
		line-height: 1.55;
	}

	/* Grid sort row */
	.sort-row {
		display: flex;
		align-items: center;
		gap: 14px;
		margin-bottom: 1.1rem;
		flex-wrap: wrap;
	}

	.sort-link {
		border: none;
		background: transparent;
		padding: 0;
		height: auto;
		font-size: 12px;
		color: var(--color-muted);
		display: inline-flex;
		align-items: center;
		gap: 3px;
	}

	.sort-link:hover {
		border: none;
		background: transparent;
		color: var(--color-ink);
	}

	.sort-link.on {
		color: var(--color-ink);
		font-weight: 600;
		text-decoration: underline;
		text-underline-offset: 3px;
	}

	.arrow {
		font-size: 10px;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
		gap: 30px 26px;
	}

	/* List */
	.list {
		display: flex;
		flex-direction: column;
	}

	.row {
		display: grid;
		gap: 18px;
		align-items: center;
		padding: 13px 0;
		border-bottom: 1px solid var(--color-rule-faint);
		position: relative;
	}

	.row.head {
		border-bottom: 1px solid var(--color-ink);
		padding: 0 0 9px;
	}

	.col-sort {
		all: unset;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		gap: 4px;
		font-size: 10px;
		font-weight: 600;
		letter-spacing: 0.11em;
		text-transform: uppercase;
		color: var(--color-faint);
	}

	.col-sort:hover,
	.col-sort.on {
		color: var(--color-ink);
	}

	.col-cover {
		width: 32px;
	}

	.row-link {
		min-width: 0;
		text-decoration: none;
		color: inherit;
	}

	.row-link:hover {
		text-decoration: none;
	}

	.row-link::after {
		content: '';
		position: absolute;
		inset: 0;
	}

	.row-title {
		font-family: var(--font-serif);
		font-size: 19px;
		line-height: 1.22;
		color: var(--color-ink);
	}

	.row-link:hover .row-title {
		color: var(--color-spot);
	}

	.row-author {
		font-size: 12px;
		color: var(--color-muted);
		margin-top: 2px;
	}

	.dim {
		color: var(--color-faint);
	}

	.col-tags {
		display: flex;
		gap: 5px;
		flex-wrap: wrap;
		position: relative;
		z-index: 1;
	}

	.col-tags button.tag {
		height: 20px;
	}

	.col-publisher {
		font-size: 12.5px;
		color: var(--color-sub);
	}

	.col-year {
		font-size: 12px;
		color: var(--color-muted);
		text-align: right;
	}

	.col-status {
		position: relative;
		z-index: 1;
	}

	.col-actions {
		position: relative;
		z-index: 1;
		text-align: right;
	}

	.quiet {
		border-color: transparent;
		background: transparent;
	}

	.quiet:hover {
		border-color: var(--color-rule);
		background: var(--color-paper-2);
	}

	/* Pagination */
	.pagination {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 15px 0 4px;
		margin-top: 4px;
		border-top: 1px solid var(--color-rule);
	}

	.range {
		font-size: 11.5px;
		color: var(--color-muted);
	}

	.pager {
		display: flex;
		align-items: center;
		gap: 14px;
	}

	.quiet-btn {
		border: none;
		background: transparent;
		padding: 0;
		height: auto;
		font-size: 11.5px;
		color: var(--color-muted);
	}

	.quiet-btn:hover:not(:disabled) {
		border: none;
		background: transparent;
		color: var(--color-ink);
	}

	.quiet-btn:disabled {
		opacity: 0.35;
		cursor: default;
	}

	.page-indicator {
		font-size: 11px;
		color: var(--color-muted);
	}

	@media (max-width: 720px) {
		.row.head {
			display: none;
		}

		.row {
			display: flex !important;
			flex-wrap: wrap;
			gap: 4px 10px;
			padding: 14px 0;
		}

		.col-cover {
			order: -1;
		}

		.row-link {
			order: -1;
			flex: 1 1 calc(100% - 42px);
		}

		.col-publisher,
		.col-year {
			font-size: 11px;
		}

		.col-tags {
			flex-basis: 100%;
			margin-left: 42px;
		}

		.col-status,
		.col-actions {
			margin-left: 42px;
		}
	}
</style>
