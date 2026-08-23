<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto, replaceState } from '$app/navigation';
	import { api } from '$lib/api';
	import type { Book, BookStats, BookStatus } from '$lib/types';
	import BookList from '$lib/components/BookList.svelte';
	import BorrowDialog from '$lib/components/BorrowDialog.svelte';
	import SearchBar from '$lib/components/SearchBar.svelte';
	import { toast } from '$lib/toast';

	const sp = page.url.searchParams;

	let books: Book[] = $state([]);
	let stats: BookStats | null = $state(null);
	let loading = $state(true);
	let borrowingBook = $state<Book | null>(null);

	let search = $state(sp.get('q') ?? '');
	let status = $state<'all' | BookStatus>((sp.get('status') as BookStatus) ?? 'all');
	let activeTags = $state<string[]>((sp.get('tags') ?? '').split(',').filter(Boolean));
	let publisher = $state(sp.get('publisher') ?? '');
	let language = $state(sp.get('language') ?? '');
	let showTagPicker = $state(false);

	let viewMode = $state<'grid' | 'list'>(sp.get('view') === 'list' ? 'list' : 'grid');
	let sortKey = $state<'title' | 'author' | 'publisher' | 'year' | 'added'>(
		(sp.get('sort') as 'title' | 'author' | 'publisher' | 'year' | 'added') ?? 'added'
	);
	let sortDir = $state<'asc' | 'desc'>(sp.get('dir') === 'asc' ? 'asc' : 'desc');
	let pageNum = $state(Number(sp.get('page')) || 1);

	async function load() {
		loading = true;
		try {
			const [b, s] = await Promise.all([
				api.books.list({ search: search || undefined }),
				api.books.stats(),
			]);
			books = b;
			stats = s;
		} catch {
			books = [];
		}
		loading = false;
	}

	onMount(load);

	// Keep the whole view state in the URL — shareable and survives reload.
	$effect(() => {
		const url = new URL(page.url);
		const p = url.searchParams;
		search ? p.set('q', search) : p.delete('q');
		status !== 'all' ? p.set('status', status) : p.delete('status');
		activeTags.length ? p.set('tags', activeTags.join(',')) : p.delete('tags');
		publisher ? p.set('publisher', publisher) : p.delete('publisher');
		language ? p.set('language', language) : p.delete('language');
		viewMode !== 'grid' ? p.set('view', viewMode) : p.delete('view');
		sortKey !== 'added' ? p.set('sort', sortKey) : p.delete('sort');
		sortDir !== 'desc' ? p.set('dir', sortDir) : p.delete('dir');
		pageNum !== 1 ? p.set('page', String(pageNum)) : p.delete('page');
		replaceState(url, {});
	});

	function bookTagsOf(b: Book): string[] {
		return b.tags ? b.tags.split(';').map((t) => t.trim()).filter(Boolean) : [];
	}

	const statusFiltered = $derived(status === 'all' ? books : books.filter((b) => b.status === status));
	const tagFiltered = $derived(
		activeTags.length ? statusFiltered.filter((b) => activeTags.every((t) => bookTagsOf(b).includes(t))) : statusFiltered
	);
	const pubFiltered = $derived(publisher ? tagFiltered.filter((b) => b.publisher === publisher) : tagFiltered);
	const finalBooks = $derived(language ? pubFiltered.filter((b) => b.language === language) : pubFiltered);

	const tagCounts = $derived.by(() => {
		const m = new Map<string, number>();
		for (const b of books) for (const t of bookTagsOf(b)) m.set(t, (m.get(t) ?? 0) + 1);
		return [...m.entries()].sort((a, b) => b[1] - a[1]);
	});
	const pickableTags = $derived(tagCounts.filter(([t]) => !activeTags.includes(t)).slice(0, 24));

	const publisherOptions = $derived.by(() =>
		[...new Set(books.map((b) => b.publisher).filter((x): x is string => !!x))].sort((a, b) => a.localeCompare(b))
	);
	const languageOptions = $derived.by(() =>
		[...new Set(books.map((b) => b.language).filter((x): x is string => !!x))].sort((a, b) => a.localeCompare(b))
	);

	const filtersActive = $derived(
		!!search || status !== 'all' || activeTags.length > 0 || !!publisher || !!language
	);
	const libraryEmpty = $derived.by(() => {
		const s = stats;
		return (s?.total ?? -1) === 0;
	});

	function setStatus(s: 'all' | BookStatus) {
		status = status === s ? 'all' : s;
		pageNum = 1;
	}

	function toggleTag(t: string) {
		activeTags = activeTags.includes(t) ? activeTags.filter((x) => x !== t) : [...activeTags, t];
		pageNum = 1;
	}

	function handleSearch(query: string) {
		search = query;
		pageNum = 1;
		load();
	}

	function clearAll() {
		search = '';
		status = 'all';
		activeTags = [];
		publisher = '';
		language = '';
		pageNum = 1;
		load();
	}

	function handleAction(action: string, book: Book) {
		if (action === 'borrow') {
			borrowingBook = book;
		} else if (action === 'return' || action === 'restore') {
			api.books
				.updateStatus(book.id, 'available')
				.then(() => {
					toast(`"${book.title}" ${action === 'return' ? 'returned' : 'restored'}.`, 'success');
					load();
				})
				.catch(() => toast(`Failed to ${action} book.`, 'error'));
		}
	}

	async function handleBorrowConfirm(borrowerName: string) {
		if (!borrowingBook) return;
		try {
			await api.books.borrow(borrowingBook.id, borrowerName);
			toast(`"${borrowingBook.title}" lent to ${borrowerName}.`, 'success');
			borrowingBook = null;
			load();
		} catch {
			toast('Failed to mark as borrowed.', 'error');
		}
	}
</script>

<svelte:head>
	<title>Catalogue — Babel</title>
</svelte:head>

<div class="page-head">
	<div>
		<h1>Catalogue</h1>
		<p class="sub">Every volume in the collection, on the shelf or out on loan.</p>
	</div>
	{#if stats}
		<div class="stat-row">
			<button class="stat-btn" class:on={status === 'all'} onclick={() => setStatus('all')}>
				<span class="num">{stats.total}</span><span class="lbl">Volumes</span>
			</button>
			<button class="stat-btn" class:on={status === 'available'} onclick={() => setStatus('available')}>
				<span class="num">{stats.available}</span><span class="lbl">On shelf</span>
			</button>
			<button class="stat-btn" class:on={status === 'borrowed'} onclick={() => setStatus('borrowed')}>
				<span class="num">{stats.borrowed}</span><span class="lbl">On loan</span>
			</button>
			<button class="stat-btn" class:on={status === 'archived'} onclick={() => setStatus('archived')}>
				<span class="num">{stats.archived}</span><span class="lbl">Archived</span>
			</button>
		</div>
	{/if}
</div>

<div class="toolbar">
	<div class="search-wrap"><SearchBar value={search} onSearch={handleSearch} /></div>
	<div class="view-toggle">
		<button class="icon-btn" class:on={viewMode === 'list'} onclick={() => (viewMode = 'list')} title="List view">
			<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/></svg>
		</button>
		<button class="icon-btn" class:on={viewMode === 'grid'} onclick={() => (viewMode = 'grid')} title="Grid view">
			<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
		</button>
	</div>
	<a href="/scan"><button>Scan</button></a>
	<a href="/books/new"><button class="primary">Add book</button></a>
</div>

<div class="filter-row">
	<span class="eyebrow">Filter</span>
	{#each activeTags as tag}
		<button class="tag on" onclick={() => toggleTag(tag)}>
			{tag}
			<svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
		</button>
	{/each}
	<div class="tag-picker">
		<button class="tag" class:on={showTagPicker} onclick={() => (showTagPicker = !showTagPicker)}>+ Tags</button>
		{#if showTagPicker}
			<div class="tag-panel">
				{#if pickableTags.length === 0}
					<span class="empty-hint">No more tags in the current results.</span>
				{/if}
				{#each pickableTags as [tag, count]}
					<button class="tag" onclick={() => toggleTag(tag)}>{tag}<span class="mono tag-count">{count}</span></button>
				{/each}
			</div>
		{/if}
	</div>
	<select class="tag select-tag" class:on={!!publisher} bind:value={publisher} onchange={() => (pageNum = 1)}>
		<option value="">All publishers</option>
		{#each publisherOptions as p}<option value={p}>{p}</option>{/each}
	</select>
	<select class="tag select-tag" class:on={!!language} bind:value={language} onchange={() => (pageNum = 1)}>
		<option value="">All languages</option>
		{#each languageOptions as l}<option value={l}>{l}</option>{/each}
	</select>
	<div class="spacer"></div>
	<span class="count">Showing <span class="mono">{finalBooks.length}</span> of <span class="mono">{books.length}</span></span>
	{#if filtersActive}
		<button class="link-btn" onclick={clearAll}>Clear</button>
	{/if}
</div>

<div class="rule-strong"></div>

{#if loading}
	<div class="loading">
		{#each Array(8) as _, i}
			<div class="skeleton-card">
				<div class="skeleton-cover"></div>
				<div class="skeleton-line" style:width="{[85, 60, 92, 70][i % 4]}%"></div>
				<div class="skeleton-line thin" style:width="{[50, 40, 55, 45][i % 4]}%"></div>
			</div>
		{/each}
	</div>
{:else}
	<BookList
		books={finalBooks}
		{viewMode}
		showActions
		onAction={handleAction}
		onTagClick={toggleTag}
		bind:sortKey
		bind:sortDir
		bind:page={pageNum}
		emptyTitle={libraryEmpty ? 'No books yet' : `No matches${search ? ` for “${search}”` : ''}`}
		emptyBody={libraryEmpty
			? 'Add your first book, or import a CSV export from your old catalogue.'
			: 'Nothing matches this search with the current filters.'}
		emptyActionLabel={libraryEmpty ? 'Add book' : filtersActive ? 'Clear filters' : undefined}
		onEmptyAction={libraryEmpty ? () => goto('/books/new') : clearAll}
	/>
{/if}

<BorrowDialog book={borrowingBook} onConfirm={handleBorrowConfirm} onClose={() => (borrowingBook = null)} />

<style>
	.page-head {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 24px;
		flex-wrap: wrap;
		padding-top: 2px;
	}

	h1 {
		font-size: 37px;
		line-height: 1.05;
	}

	.sub {
		font-size: 12.5px;
		color: var(--color-muted);
		margin-top: 7px;
	}

	.stat-row {
		display: flex;
		align-items: flex-end;
		gap: 22px;
	}

	.stat-btn {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 1px;
		border: none;
		background: transparent;
		height: auto;
		padding: 0 0 3px;
		border-bottom: 1.5px solid transparent;
	}

	.stat-btn:hover {
		border: none;
		border-bottom: 1.5px solid var(--color-rule-strong);
		background: transparent;
	}

	.stat-btn.on {
		border-bottom: 1.5px solid var(--color-ink);
	}

	.num {
		font-family: var(--font-serif);
		font-size: 23px;
		line-height: 1;
		color: var(--color-ink);
	}

	.lbl {
		font-size: 9px;
		font-weight: 600;
		letter-spacing: 0.09em;
		text-transform: uppercase;
		color: var(--color-faint);
	}

	.stat-btn.on .lbl {
		color: var(--color-muted);
	}

	.toolbar {
		display: flex;
		align-items: center;
		gap: 14px;
		padding-top: 22px;
	}

	.search-wrap {
		flex: 1;
		min-width: 0;
	}

	.view-toggle {
		display: flex;
		gap: 2px;
	}

	.icon-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 31px;
		padding: 0;
		border-color: transparent;
		color: var(--color-faint);
	}

	.icon-btn.on {
		border-color: var(--color-ink);
		color: var(--color-ink);
	}

	.filter-row {
		display: flex;
		align-items: center;
		gap: 9px;
		flex-wrap: wrap;
		padding: 14px 0;
	}

	.tag-picker {
		position: relative;
	}

	.tag-panel {
		position: absolute;
		top: calc(100% + 8px);
		left: 0;
		z-index: 20;
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		width: 380px;
		max-height: 220px;
		overflow-y: auto;
		padding: 12px;
		background: var(--color-paper);
		border: 1px solid var(--color-ink);
		box-shadow: var(--shadow);
	}

	.empty-hint {
		font-size: 11.5px;
		color: var(--color-faint);
	}

	.tag-count {
		font-size: 10.5px;
		color: var(--color-faint);
		margin-left: 1px;
	}

	select.tag {
		width: auto;
		height: 22px;
		padding-right: 4px;
		font-family: inherit;
	}

	.spacer {
		flex: 1;
	}

	.count {
		font-size: 11.5px;
		color: var(--color-muted);
	}

	.link-btn {
		border: none;
		background: transparent;
		height: auto;
		padding: 0;
		font-size: 11.5px;
		color: var(--color-spot);
		text-decoration: underline;
		text-underline-offset: 3px;
	}

	.link-btn:hover {
		border: none;
		background: transparent;
		color: var(--color-spot);
	}

	.rule-strong {
		height: 1px;
		background: var(--color-ink);
		margin-bottom: 22px;
	}

	.loading {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
		gap: 30px 26px;
	}

	.skeleton-card {
		display: flex;
		flex-direction: column;
		gap: 9px;
	}

	.skeleton-cover {
		aspect-ratio: 2 / 3;
		background: linear-gradient(100deg, var(--color-rule-faint) 30%, var(--color-paper-2) 50%, var(--color-rule-faint) 70%);
		background-size: 200% 100%;
		animation: shimmer 1.4s ease-in-out infinite;
	}

	.skeleton-line {
		height: 12px;
		background: var(--color-rule-faint);
	}

	.skeleton-line.thin {
		height: 9px;
		opacity: 0.7;
	}

	@keyframes shimmer {
		0% { background-position: 200% 0; }
		100% { background-position: -200% 0; }
	}

	@media (max-width: 720px) {
		.page-head {
			flex-direction: column;
			align-items: flex-start;
			gap: 14px;
		}

		.stat-row {
			gap: 18px;
			max-width: 100%;
			overflow-x: auto;
			padding-bottom: 2px;
		}

		.stat-btn {
			flex: none;
		}

		.view-toggle {
			display: none;
		}

		.toolbar {
			flex-wrap: wrap;
		}

		.search-wrap {
			flex-basis: 100%;
			order: -1;
		}

		/* Force the count/clear onto their own line rather than fighting
		   the filter chips for space on a narrow viewport. */
		.filter-row .spacer {
			flex-basis: 100%;
			height: 0;
		}
	}
</style>
