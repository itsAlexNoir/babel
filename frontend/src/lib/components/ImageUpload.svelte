<script lang="ts">
	let { files = $bindable([]), accept = 'image/*', multiple = true }: {
		files: File[];
		accept?: string;
		multiple?: boolean;
	} = $props();

	let dragging = $state(false);
	let inputEl: HTMLInputElement;

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		dragging = false;
		if (e.dataTransfer?.files) {
			addFiles(Array.from(e.dataTransfer.files));
		}
	}

	function handleSelect(e: Event) {
		const target = e.target as HTMLInputElement;
		if (target.files) {
			addFiles(Array.from(target.files));
		}
	}

	function addFiles(newFiles: File[]) {
		const imageFiles = newFiles.filter(f => f.type.startsWith('image/'));
		files = multiple ? [...files, ...imageFiles] : imageFiles.slice(0, 1);
	}

	function removeFile(index: number) {
		files = files.filter((_, i) => i !== index);
	}
</script>

<div class="upload-area" class:dragging
	role="button"
	tabindex="0"
	ondragover={(e) => { e.preventDefault(); dragging = true; }}
	ondragleave={() => dragging = false}
	ondrop={handleDrop}
	onclick={() => inputEl.click()}
	onkeydown={(e) => { if (e.key === 'Enter') inputEl.click(); }}
>
	<input bind:this={inputEl} type="file" {accept} {multiple} onchange={handleSelect} hidden />
	<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
	<p>Drop images here or click to browse</p>
	<span class="hint">Supports JPEG, PNG, WebP</span>
</div>

{#if files.length > 0}
	<div class="previews">
		{#each files as file, i}
			<div class="preview">
				<img src={URL.createObjectURL(file)} alt={file.name} />
				<button class="remove" onclick={() => removeFile(i)}>&times;</button>
			</div>
		{/each}
	</div>
{/if}

<style>
	.upload-area {
		border: 2px dashed var(--color-border);
		border-radius: var(--radius);
		padding: 2rem;
		text-align: center;
		cursor: pointer;
		transition: all 0.15s ease;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
		color: var(--color-text-secondary);
	}

	.upload-area:hover, .upload-area.dragging {
		border-color: var(--color-primary);
		background: rgba(37, 99, 235, 0.03);
	}

	.upload-area p {
		font-size: 0.9rem;
		font-weight: 500;
	}

	.hint {
		font-size: 0.75rem;
	}

	.previews {
		display: flex;
		gap: 0.75rem;
		margin-top: 1rem;
		flex-wrap: wrap;
	}

	.preview {
		position: relative;
		width: 80px;
		height: 80px;
		border-radius: var(--radius);
		overflow: hidden;
		border: 1px solid var(--color-border);
	}

	.preview img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.remove {
		position: absolute;
		top: 2px;
		right: 2px;
		width: 20px;
		height: 20px;
		padding: 0;
		border-radius: 50%;
		background: rgba(0,0,0,0.6);
		color: white;
		border: none;
		font-size: 14px;
		line-height: 1;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
