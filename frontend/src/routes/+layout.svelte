<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';
	import Toast from '$lib/components/Toast.svelte';

	let { children } = $props();

	// Borrowed and Archived are status facets of the Catalogue now (see /books),
	// not separate destinations — /borrowed and /archived still work as deep links.
	const NAV = [
		{ href: '/books', label: 'Catalogue' },
		{ href: '/scan', label: 'Scan' },
		{ href: '/data', label: 'Import' },
		{ href: '/stats', label: 'Statistics' },
	];

	const TABS = [
		{ href: '/books', label: 'Catalogue', icon: 'books' },
		{ href: '/scan', label: 'Scan', icon: 'scan' },
		{ href: '/stats', label: 'Stats', icon: 'chart' },
		{ href: '/data', label: 'Import', icon: 'data' },
	];

	function isActive(href: string): boolean {
		return page.url.pathname === href || page.url.pathname.startsWith(href + '/');
	}
</script>

<svelte:head>
	<title>Babel — Library Catalogue</title>
</svelte:head>

<div class="shell">
	<header class="masthead">
		<div class="masthead-top">
			<a href="/" class="wordmark">
				<span class="wordmark-text">Babel</span>
				<span class="wordmark-sub">Library catalogue</span>
			</a>
		</div>
		<div class="rule-strong"></div>
		<nav class="tabs">
			{#each NAV as item}
				<a
					href={item.href}
					class="tab"
					class:on={isActive(item.href)}
					aria-current={isActive(item.href) ? 'page' : undefined}
				>
					{item.label}
				</a>
			{/each}
		</nav>
	</header>

	<main class="content">
		{@render children()}
	</main>

	<nav class="mobile-tabs" aria-label="Primary">
		{#each TABS as item}
			<a href={item.href} class="mobile-tab" class:on={isActive(item.href)} aria-current={isActive(item.href) ? 'page' : undefined}>
				{#if item.icon === 'books'}
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>
				{:else if item.icon === 'scan'}
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8V5a2 2 0 0 1 2-2h3"/><path d="M16 3h3a2 2 0 0 1 2 2v3"/><path d="M21 16v3a2 2 0 0 1-2 2h-3"/><path d="M8 21H5a2 2 0 0 1-2-2v-3"/></svg>
				{:else if item.icon === 'chart'}
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><rect x="7" y="12" width="3" height="5"/><rect x="13" y="8" width="3" height="9"/><rect x="19" y="5" width="3" height="12"/></svg>
				{:else}
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>
				{/if}
				<span>{item.label}</span>
			</a>
		{/each}
	</nav>
</div>

<Toast />

<style>
	.shell {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	.masthead {
		flex: none;
		padding: 0 56px;
		background: var(--color-paper);
		position: sticky;
		top: 0;
		z-index: 10;
	}

	.masthead-top {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		padding: 22px 0 12px;
	}

	.wordmark {
		display: flex;
		align-items: baseline;
		gap: 13px;
		text-decoration: none;
		color: var(--color-ink);
	}

	.wordmark:hover {
		text-decoration: none;
	}

	.wordmark-text {
		font-family: var(--font-serif);
		font-size: 29px;
		line-height: 1;
	}

	.wordmark-sub {
		font-size: 9.5px;
		font-weight: 600;
		letter-spacing: 0.11em;
		text-transform: uppercase;
		color: var(--color-faint);
	}

	.rule-strong {
		height: 1.5px;
		background: var(--color-ink);
	}

	.tabs {
		display: flex;
		gap: 26px;
		padding-top: 11px;
		border-bottom: 1px solid var(--color-rule);
		overflow-x: auto;
	}

	.tab {
		position: relative;
		font-size: 13px;
		font-weight: 500;
		color: var(--color-muted);
		text-decoration: none;
		padding-bottom: 10px;
		white-space: nowrap;
	}

	.tab:hover {
		color: var(--color-ink);
		text-decoration: none;
	}

	.tab.on {
		color: var(--color-ink);
		font-weight: 600;
	}

	.tab.on::after {
		content: '';
		position: absolute;
		left: 0;
		right: 0;
		bottom: -1px;
		height: 1.5px;
		background: var(--color-ink);
	}

	.content {
		flex: 1;
		width: 100%;
		max-width: 1440px;
		padding: 28px 56px 56px;
	}

	.mobile-tabs {
		display: none;
	}

	@media (max-width: 768px) {
		.masthead {
			padding: 0 20px;
		}

		.masthead-top {
			padding: 16px 0 10px;
		}

		.wordmark-text {
			font-size: 24px;
		}

		.tabs {
			display: none;
		}

		.content {
			padding: 18px 20px 78px;
		}

		.mobile-tabs {
			display: flex;
			position: fixed;
			bottom: 0;
			left: 0;
			right: 0;
			background: var(--color-paper);
			border-top: 1px solid var(--color-rule);
			padding: 3px 3px calc(env(safe-area-inset-bottom, 0px) + 8px);
			z-index: 10;
		}

		.mobile-tab {
			flex: 1;
			min-height: 54px;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			gap: 4px;
			text-decoration: none;
			color: var(--color-faint);
			position: relative;
			font-size: 10px;
			font-weight: 500;
		}

		.mobile-tab:hover {
			text-decoration: none;
		}

		.mobile-tab.on {
			color: var(--color-ink);
			font-weight: 600;
		}

		.mobile-tab.on::before {
			content: '';
			position: absolute;
			top: 0;
			width: 24px;
			height: 1.5px;
			background: var(--color-ink);
		}
	}
</style>
