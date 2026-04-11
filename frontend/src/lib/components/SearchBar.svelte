<script lang="ts">
	let { value = '', placeholder = 'Search by title or author...', onSearch }: {
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
</script>

<div class="search-bar">
	<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
	<input type="text" {placeholder} {value} oninput={handleInput} />
</div>

<style>
	.search-bar {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 0 0.75rem;
	}

	.search-bar svg {
		color: var(--color-text-secondary);
		flex-shrink: 0;
	}

	.search-bar input {
		border: none;
		padding: 0.6rem 0;
		background: transparent;
	}

	.search-bar input:focus {
		box-shadow: none;
	}
</style>
