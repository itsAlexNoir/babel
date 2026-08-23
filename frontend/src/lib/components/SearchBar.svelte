<script lang="ts">
	let { value = '', placeholder = 'Search titles, authors, publishers…', onSearch }: {
		value?: string;
		placeholder?: string;
		onSearch: (query: string) => void;
	} = $props();

	let timeout: ReturnType<typeof setTimeout>;

	function handleInput(e: Event) {
		const target = e.target as HTMLInputElement;
		value = target.value;
		clearTimeout(timeout);
		timeout = setTimeout(() => onSearch(value), 300);
	}

	function clear() {
		value = '';
		clearTimeout(timeout);
		onSearch('');
	}
</script>

<div class="search-bar">
	<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
	<input type="text" {placeholder} {value} oninput={handleInput} />
	{#if value}
		<button class="clear" onclick={clear} aria-label="Clear search">
			<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
		</button>
	{/if}
</div>

<style>
	.search-bar {
		display: flex;
		align-items: center;
		gap: 9px;
		border-bottom: 1px solid var(--color-rule);
		height: 38px;
	}

	.search-bar:focus-within {
		border-bottom-color: var(--color-ink);
	}

	.search-bar svg {
		color: var(--color-faint);
		flex-shrink: 0;
	}

	.search-bar input {
		border: none;
		padding: 0;
		background: transparent;
		font-size: 15px;
	}

	.search-bar input:focus {
		border: none;
	}

	.clear {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 22px;
		height: 22px;
		padding: 0;
		border: none;
		background: transparent;
		color: var(--color-faint);
		flex-shrink: 0;
	}

	.clear:hover {
		border: none;
		background: transparent;
		color: var(--color-ink);
	}
</style>
