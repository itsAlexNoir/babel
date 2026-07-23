<script lang="ts">
	import { api } from '$lib/api';
	import { toast } from '$lib/toast';
	import type { ImportResult } from '$lib/types';

	let csvFile: File | null = $state(null);
	let importing = $state(false);
	let importResult: ImportResult | null = $state(null);
	let exportFormat = $state('json');

	function onFileChange(e: Event) {
		const input = e.target as HTMLInputElement;
		csvFile = input.files?.[0] ?? null;
		importResult = null;
	}

	async function handleImport() {
		if (!csvFile) return;
		importing = true;
		importResult = null;
		try {
			importResult = await api.data.importCsv(csvFile);
			toast(`Imported ${importResult.added} books`, 'success');
		} catch (err: any) {
			toast(err.message || 'Import failed', 'error');
		} finally {
			importing = false;
		}
	}

	function handleExport() {
		window.open(api.data.exportUrl(exportFormat), '_blank');
	}

	function handleBackup() {
		window.open(api.data.backupUrl(), '_blank');
	}
</script>

<div class="data-page">
	<h1>Data Management</h1>

	<!-- Import CSV -->
	<section class="card">
		<h2>Import CSV</h2>
		<p class="description">
			Import books from a CSV with columns: autor/a, título, título original, editorial,
			traductor/a, año publicacion, año edicion, idioma, etiquetas.
		</p>
		<div class="import-controls">
			<input type="file" accept=".csv" onchange={onFileChange} />
			<button class="primary" onclick={handleImport} disabled={!csvFile || importing}>
				{importing ? 'Importing…' : 'Import'}
			</button>
		</div>
		{#if importResult}
			<div class="result">
				<span class="result-item success">Added: {importResult.added}</span>
				<span class="result-item">Duplicates skipped: {importResult.skipped_duplicate}</span>
				<span class="result-item">Missing title: {importResult.skipped_missing}</span>
				{#if importResult.errors > 0}
					<span class="result-item error">Errors: {importResult.errors}</span>
				{/if}
			</div>
		{/if}
	</section>

	<!-- Export Database -->
	<section class="card">
		<h2>Export Database</h2>
		<p class="description">Download the full catalogue in your preferred format.</p>
		<div class="export-controls">
			<select bind:value={exportFormat}>
				<option value="json">JSON</option>
				<option value="csv">CSV</option>
				<option value="jsonl">JSONL</option>
			</select>
			<button class="primary" onclick={handleExport}>Download Export</button>
		</div>
	</section>

	<!-- Backup -->
	<section class="card">
		<h2>Database Backup</h2>
		<p class="description">Download a raw copy of the SQLite database file.</p>
		<button class="primary" onclick={handleBackup}>Download Backup</button>
	</section>
</div>

<style>
	.data-page {
		max-width: 700px;
	}

	h1 {
		font-size: 1.5rem;
		font-weight: 600;
		margin-bottom: 1.5rem;
	}

	.card {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1.5rem;
		margin-bottom: 1.25rem;
	}

	.card h2 {
		font-size: 1.1rem;
		font-weight: 600;
		margin-bottom: 0.5rem;
	}

	.description {
		color: var(--color-text-secondary);
		font-size: 0.85rem;
		margin-bottom: 1rem;
	}

	.import-controls,
	.export-controls {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		flex-wrap: wrap;
	}

	select {
		padding: 0.5rem 0.75rem;
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		background: var(--color-bg);
		color: var(--color-text);
		font-size: 0.9rem;
	}

	.result {
		display: flex;
		gap: 1rem;
		margin-top: 1rem;
		flex-wrap: wrap;
		font-size: 0.85rem;
	}

	.result-item {
		padding: 0.35rem 0.75rem;
		border-radius: var(--radius);
		background: var(--color-bg);
		border: 1px solid var(--color-border);
	}

	.result-item.success {
		border-color: var(--color-success);
		color: var(--color-success);
	}

	.result-item.error {
		border-color: var(--color-danger);
		color: var(--color-danger);
	}
</style>
