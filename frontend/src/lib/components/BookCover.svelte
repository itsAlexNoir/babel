<script lang="ts">
	import type { Book } from '$lib/types';
	import { coverTint } from '$lib/coverPalette';

	let { book, size = 'm' }: {
		book: Book;
		size?: 's' | 'm' | 'l';
	} = $props();

	const coverUrl = $derived(book.cover_image_path ? `/uploads/${book.cover_image_path}` : null);
	const tint = $derived(coverTint(book.title));
</script>

{#if coverUrl}
	<div class="cover img">
		<img src={coverUrl} alt="{book.title} cover" />
	</div>
{:else if size === 's'}
	<!-- Too narrow to set type legibly — a plain tinted swatch with a mark, matching the row thumb. -->
	<div class="cover generated s swatch" style:background={tint.ground} style:color={tint.ink} title={book.title}>
		<div class="mark"></div>
	</div>
{:else}
	<div class="cover generated {size}" style:background={tint.ground} style:color={tint.ink}>
		<div class="title">{book.title}</div>
		<div class="foot">
			<div class="rule"></div>
			<div class="author">{book.author}</div>
			{#if book.publisher}
				<div class="publisher">{book.publisher}</div>
			{/if}
		</div>
	</div>
{/if}

<style>
	.cover {
		aspect-ratio: 2 / 3;
		overflow: hidden;
		flex: none;
	}

	.cover.img img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.cover.generated {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.cover.generated.s {
		padding: 8px 7px;
	}

	.cover.generated.m {
		padding: 13px 12px;
	}

	.cover.generated.l {
		padding: 22px 19px;
	}

	.cover.generated.swatch {
		padding: 0;
		align-items: center;
		justify-content: center;
	}

	.mark {
		width: 40%;
		height: 1px;
		background: currentColor;
		opacity: 0.5;
	}

	.title {
		font-family: var(--font-serif);
		line-height: 1.18;
		display: -webkit-box;
		-webkit-line-clamp: 5;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}

	.m .title {
		font-size: 15px;
	}

	.l .title {
		font-size: 23px;
	}

	.foot {
		display: flex;
		flex-direction: column;
		gap: 5px;
	}

	.l .foot {
		gap: 7px;
	}

	.rule {
		height: 1px;
		background: currentColor;
		opacity: 0.35;
	}

	.author {
		font-weight: 500;
		opacity: 0.82;
	}

	.m .author {
		font-size: 11px;
	}

	.l .author {
		font-size: 14px;
	}

	.publisher {
		font-weight: 600;
		letter-spacing: 0.11em;
		text-transform: uppercase;
		opacity: 0.6;
	}

	.m .publisher {
		font-size: 8.5px;
	}

	.l .publisher {
		font-size: 10px;
	}
</style>
