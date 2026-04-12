<script lang="ts">
	import '../app.css';
	import Toast from '$lib/components/Toast.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<title>Babel — Library Catalogue</title>
</svelte:head>

<div class="app">
	<nav class="sidebar">
		<a href="/" class="logo">
			<span class="logo-icon">📚</span>
			<span class="logo-text">Babel</span>
		</a>
		<div class="nav-links">
			<a href="/books" class="nav-link">
				<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>
				Catalogue
			</a>
			<a href="/borrowed" class="nav-link">
				<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
				Borrowed
			</a>
			<a href="/archived" class="nav-link">
				<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="5" x="2" y="3" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/></svg>
				Archived
			</a>
			<a href="/scan" class="nav-link">
				<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 12a1 1 0 0 0-1 1v1a1 1 0 0 1-1 1 1 1 0 0 1 1 1v1a1 1 0 0 0 1 1"/><path d="M14 18a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1 1 1 0 0 1-1-1v-1a1 1 0 0 0-1-1"/></svg>
				Scan
			</a>
			<a href="/data" class="nav-link">
				<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>
				Data
			</a>
		</div>
	</nav>
	<main class="content">
		{@render children()}
	</main>
</div>

<Toast />

<style>
	.app {
		display: flex;
		min-height: 100vh;
	}

	.sidebar {
		width: 220px;
		background: var(--color-surface);
		border-right: 1px solid var(--color-border);
		padding: 1.5rem 1rem;
		display: flex;
		flex-direction: column;
		gap: 2rem;
		position: fixed;
		top: 0;
		left: 0;
		bottom: 0;
		z-index: 10;
	}

	.logo {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		text-decoration: none;
		color: var(--color-text);
	}

	.logo-icon {
		font-size: 1.5rem;
	}

	.logo-text {
		font-size: 1.25rem;
		font-weight: 600;
	}

	.nav-links {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.nav-link {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.6rem 0.75rem;
		border-radius: var(--radius);
		color: var(--color-text-secondary);
		text-decoration: none;
		font-size: 0.9rem;
		font-weight: 500;
		transition: all 0.15s ease;
	}

	.nav-link:hover {
		background: var(--color-bg);
		color: var(--color-text);
		text-decoration: none;
	}

	.content {
		flex: 1;
		margin-left: 220px;
		padding: 2rem;
		max-width: 1200px;
	}

	@media (max-width: 768px) {
		.sidebar {
			position: fixed;
			bottom: 0;
			top: auto;
			left: 0;
			right: 0;
			width: 100%;
			flex-direction: row;
			padding: 0.5rem 1rem;
			gap: 0;
			border-right: none;
			border-top: 1px solid var(--color-border);
			justify-content: center;
		}

		.logo {
			display: none;
		}

		.nav-links {
			flex-direction: row;
			gap: 0.5rem;
		}

		.nav-link {
			flex-direction: column;
			gap: 0.25rem;
			font-size: 0.7rem;
			padding: 0.4rem 0.75rem;
		}

		.content {
			margin-left: 0;
			padding: 1rem;
			padding-bottom: 5rem;
		}
	}
</style>
