<script lang="ts">
	import { toasts } from '$lib/toast';
</script>

{#if $toasts.length > 0}
	<div class="toast-container">
		{#each $toasts as t (t.id)}
			<div class="toast {t.type}">
				{t.message}
			</div>
		{/each}
	</div>
{/if}

<style>
	.toast-container {
		position: fixed;
		top: 1rem;
		right: 1rem;
		z-index: 1000;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.toast {
		padding: 0.75rem 1.25rem;
		border-radius: var(--radius);
		font-size: 0.875rem;
		font-weight: 500;
		box-shadow: var(--shadow);
		animation: slide-in 0.2s ease-out;
	}

	.toast.success {
		background: #dcfce7;
		color: #166534;
		border: 1px solid #bbf7d0;
	}

	.toast.error {
		background: #fef2f2;
		color: #991b1b;
		border: 1px solid #fecaca;
	}

	.toast.info {
		background: #eff6ff;
		color: #1e40af;
		border: 1px solid #bfdbfe;
	}

	@keyframes slide-in {
		from {
			transform: translateX(100%);
			opacity: 0;
		}
		to {
			transform: translateX(0);
			opacity: 1;
		}
	}
</style>
