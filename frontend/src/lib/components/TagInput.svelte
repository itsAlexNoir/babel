<script lang="ts">
	// Presents the semicolon-separated `tags` string the API stores as a row
	// of removable chips instead of raw text — the value stays a plain
	// "a; b; c" string on the wire, so nothing on the backend has to change.
	let { value = $bindable(''), id, placeholder = 'Add tag…' }: {
		value?: string;
		id?: string;
		placeholder?: string;
	} = $props();

	let tags = $state<string[]>(
		value ? value.split(';').map((t) => t.trim()).filter(Boolean) : []
	);
	let draft = $state('');
	let inputEl: HTMLInputElement | undefined = $state();

	$effect(() => {
		value = tags.join('; ');
	});

	function commitDraft() {
		const t = draft.trim();
		if (t && !tags.includes(t)) tags = [...tags, t];
		draft = '';
	}

	function removeTag(i: number) {
		tags = tags.filter((_, idx) => idx !== i);
		inputEl?.focus();
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ',' || e.key === ';') {
			e.preventDefault();
			commitDraft();
		} else if (e.key === 'Backspace' && draft === '' && tags.length > 0) {
			e.preventDefault();
			tags = tags.slice(0, -1);
		}
	}
</script>

<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
<div class="tag-input" onclick={() => inputEl?.focus()}>
	{#each tags as tag, i}
		<span class="chip">
			{tag}
			<button type="button" onclick={() => removeTag(i)} aria-label="Remove {tag}">
				<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
			</button>
		</span>
	{/each}
	<input
		bind:this={inputEl}
		{id}
		type="text"
		bind:value={draft}
		onkeydown={handleKeydown}
		onblur={commitDraft}
		placeholder={tags.length ? '' : placeholder}
	/>
</div>

<style>
	.tag-input {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 6px;
		min-height: 36px;
		padding: 5px 0;
		border-bottom: 1px solid var(--color-rule);
		cursor: text;
	}

	.tag-input:focus-within {
		border-bottom-color: var(--color-ink);
	}

	.chip {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		height: 22px;
		padding: 0 4px 0 8px;
		border: 1px solid var(--color-ink);
		border-radius: var(--radius);
		background: var(--color-ink);
		color: var(--color-paper);
		font-size: 11.5px;
		white-space: nowrap;
	}

	.chip button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 16px;
		height: 16px;
		padding: 0;
		border: none;
		background: transparent;
		color: currentColor;
		opacity: 0.65;
	}

	.chip button:hover {
		border: none;
		background: transparent;
		opacity: 1;
	}

	input {
		flex: 1;
		min-width: 90px;
		border: none;
		padding: 0;
		height: 22px;
		font-size: 13.5px;
	}

	input:focus {
		border: none;
	}
</style>
