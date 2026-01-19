# Supabase Storage

Bucket organisation, policies, and upload patterns for e-commerce.

## Bucket Structure

```
storage/
├── product-images/     # Public - product photos
│   ├── {product_id}/
│   │   ├── main.webp
│   │   ├── gallery-1.webp
│   │   └── gallery-2.webp
├── cms-images/         # Public - CMS content images
│   ├── hero/
│   ├── about/
│   └── banners/
├── category-images/    # Public - category banners
│   └── {category_slug}.webp
└── order-attachments/  # Private - order-related files
    └── {order_id}/
```

## Bucket Creation

```sql
-- Product images (public read, admin write)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'product-images',
  'product-images',
  true,
  5242880,  -- 5MB limit
  ARRAY['image/jpeg', 'image/png', 'image/webp', 'image/avif']
);

-- CMS images (public read, admin write)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'cms-images',
  'cms-images',
  true,
  10485760,  -- 10MB limit
  ARRAY['image/jpeg', 'image/png', 'image/webp', 'image/avif', 'image/svg+xml']
);

-- Category images (public read, admin write)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'category-images',
  'category-images',
  true,
  5242880,
  ARRAY['image/jpeg', 'image/png', 'image/webp', 'image/avif']
);

-- Order attachments (private - authenticated access only)
INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES (
  'order-attachments',
  'order-attachments',
  false,
  20971520  -- 20MB limit
);
```

## Storage Policies

### Public Buckets (product-images, cms-images, category-images)

```sql
-- Anyone can view public bucket images
CREATE POLICY "Public read access"
ON storage.objects FOR SELECT
USING (bucket_id IN ('product-images', 'cms-images', 'category-images'));

-- Only admins can upload to public buckets
CREATE POLICY "Admin upload access"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id IN ('product-images', 'cms-images', 'category-images')
  AND EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_id = auth.uid()
    AND role_id IN ('super_admin', 'admin', 'shop_editor', 'cms_editor')
  )
);

-- Only admins can update/replace images
CREATE POLICY "Admin update access"
ON storage.objects FOR UPDATE
USING (
  bucket_id IN ('product-images', 'cms-images', 'category-images')
  AND EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_id = auth.uid()
    AND role_id IN ('super_admin', 'admin', 'shop_editor', 'cms_editor')
  )
);

-- Only admins can delete images
CREATE POLICY "Admin delete access"
ON storage.objects FOR DELETE
USING (
  bucket_id IN ('product-images', 'cms-images', 'category-images')
  AND EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_id = auth.uid()
    AND role_id IN ('super_admin', 'admin', 'shop_editor', 'cms_editor')
  )
);
```

### Private Bucket (order-attachments)

```sql
-- Users can view their own order attachments
CREATE POLICY "Users view own order attachments"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'order-attachments'
  AND (
    -- Extract order_id from path and check ownership
    EXISTS (
      SELECT 1 FROM orders
      WHERE orders.id::text = (storage.foldername(name))[1]
      AND (orders.user_id = auth.uid() OR orders.customer_email = auth.jwt()->>'email')
    )
    OR
    -- Admins can view all
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_id = auth.uid()
      AND role_id IN ('super_admin', 'admin', 'shop_editor')
    )
  )
);

-- Only admins can upload order attachments
CREATE POLICY "Admin upload order attachments"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'order-attachments'
  AND EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_id = auth.uid()
    AND role_id IN ('super_admin', 'admin', 'shop_editor')
  )
);
```

## Image Upload Utilities

### Storage Helper Library

```typescript
// src/lib/storage.ts
import { supabase } from './supabase';

export type ImageBucket = 'product-images' | 'cms-images' | 'category-images';

interface UploadResult {
  path: string;
  publicUrl: string;
}

/**
 * Upload image to Supabase Storage
 */
export async function uploadImage(
  bucket: ImageBucket,
  file: File,
  path: string
): Promise<UploadResult> {
  // Generate optimised filename
  const ext = file.name.split('.').pop()?.toLowerCase() || 'webp';
  const filename = `${path}.${ext}`;

  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(filename, file, {
      cacheControl: '31536000', // 1 year cache
      upsert: true,
    });

  if (error) throw error;

  const { data: urlData } = supabase.storage
    .from(bucket)
    .getPublicUrl(data.path);

  return {
    path: data.path,
    publicUrl: urlData.publicUrl,
  };
}

/**
 * Upload product image with proper path structure
 */
export async function uploadProductImage(
  productId: string,
  file: File,
  type: 'main' | 'gallery',
  index?: number
): Promise<UploadResult> {
  const filename = type === 'main'
    ? 'main'
    : `gallery-${index ?? Date.now()}`;

  return uploadImage('product-images', file, `${productId}/${filename}`);
}

/**
 * Upload CMS image with folder organisation
 */
export async function uploadCmsImage(
  folder: string,
  file: File,
  name?: string
): Promise<UploadResult> {
  const filename = name || `${Date.now()}-${file.name.replace(/\s+/g, '-')}`;
  return uploadImage('cms-images', file, `${folder}/${filename}`);
}

/**
 * Upload category image
 */
export async function uploadCategoryImage(
  categorySlug: string,
  file: File
): Promise<UploadResult> {
  return uploadImage('category-images', file, categorySlug);
}

/**
 * Delete image from storage
 */
export async function deleteImage(
  bucket: ImageBucket,
  path: string
): Promise<void> {
  const { error } = await supabase.storage
    .from(bucket)
    .remove([path]);

  if (error) throw error;
}

/**
 * Get public URL for image
 */
export function getImageUrl(bucket: ImageBucket, path: string): string {
  const { data } = supabase.storage.from(bucket).getPublicUrl(path);
  return data.publicUrl;
}

/**
 * List images in folder
 */
export async function listImages(
  bucket: ImageBucket,
  folder: string
): Promise<string[]> {
  const { data, error } = await supabase.storage
    .from(bucket)
    .list(folder);

  if (error) throw error;

  return (data || [])
    .filter(item => !item.id.endsWith('/'))
    .map(item => `${folder}/${item.name}`);
}
```

### Image Upload Component (Admin)

```typescript
// src/components/admin/ImageUpload.tsx
'use client';

import { useState, useCallback } from 'react';
import { uploadImage, type ImageBucket } from '@/lib/storage';
import Image from 'next/image';

interface ImageUploadProps {
  bucket: ImageBucket;
  path: string;
  currentUrl?: string;
  onUpload: (url: string, path: string) => void;
  onError?: (error: Error) => void;
  accept?: string;
  maxSize?: number; // in MB
}

export function ImageUpload({
  bucket,
  path,
  currentUrl,
  onUpload,
  onError,
  accept = 'image/jpeg,image/png,image/webp',
  maxSize = 5,
}: ImageUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState<string | null>(currentUrl || null);
  const [dragOver, setDragOver] = useState(false);

  const handleUpload = useCallback(async (file: File) => {
    // Validate file size
    if (file.size > maxSize * 1024 * 1024) {
      onError?.(new Error(`File must be under ${maxSize}MB`));
      return;
    }

    // Validate file type
    if (!accept.split(',').some(type => file.type === type.trim())) {
      onError?.(new Error('Invalid file type'));
      return;
    }

    setUploading(true);

    try {
      // Show preview immediately
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target?.result as string);
      reader.readAsDataURL(file);

      // Upload to Supabase
      const result = await uploadImage(bucket, file, path);
      onUpload(result.publicUrl, result.path);
    } catch (error) {
      onError?.(error as Error);
      setPreview(currentUrl || null);
    } finally {
      setUploading(false);
    }
  }, [bucket, path, currentUrl, onUpload, onError, accept, maxSize]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleUpload(file);
  }, [handleUpload]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleUpload(file);
  }, [handleUpload]);

  return (
    <div
      className={`
        relative border-2 border-dashed rounded-lg p-4 text-center
        transition-colors cursor-pointer
        ${dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
        ${uploading ? 'opacity-50 pointer-events-none' : ''}
      `}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
    >
      <input
        type="file"
        accept={accept}
        onChange={handleChange}
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        disabled={uploading}
      />

      {preview ? (
        <div className="relative aspect-video w-full max-w-xs mx-auto">
          <Image
            src={preview}
            alt="Preview"
            fill
            className="object-contain rounded"
          />
        </div>
      ) : (
        <div className="py-8">
          <svg
            className="w-12 h-12 mx-auto text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          <p className="mt-2 text-sm text-gray-600">
            Drag & drop or click to upload
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Max {maxSize}MB • JPEG, PNG, WebP
          </p>
        </div>
      )}

      {uploading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/80 rounded-lg">
          <div className="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full" />
        </div>
      )}
    </div>
  );
}
```

### Multi-Image Gallery Upload

```typescript
// src/components/admin/GalleryUpload.tsx
'use client';

import { useState } from 'react';
import { uploadProductImage, deleteImage } from '@/lib/storage';
import Image from 'next/image';

interface GalleryUploadProps {
  productId: string;
  images: string[];
  onChange: (images: string[]) => void;
  maxImages?: number;
}

export function GalleryUpload({
  productId,
  images,
  onChange,
  maxImages = 10,
}: GalleryUploadProps) {
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (files: FileList) => {
    if (images.length + files.length > maxImages) {
      alert(`Maximum ${maxImages} images allowed`);
      return;
    }

    setUploading(true);
    const newUrls: string[] = [];

    try {
      for (let i = 0; i < files.length; i++) {
        const result = await uploadProductImage(
          productId,
          files[i],
          'gallery',
          images.length + i
        );
        newUrls.push(result.publicUrl);
      }
      onChange([...images, ...newUrls]);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleRemove = async (index: number) => {
    const imageUrl = images[index];
    // Extract path from URL for deletion
    const path = new URL(imageUrl).pathname.split('/').slice(-2).join('/');

    try {
      await deleteImage('product-images', path);
      onChange(images.filter((_, i) => i !== index));
    } catch (error) {
      console.error('Delete failed:', error);
    }
  };

  const handleReorder = (fromIndex: number, toIndex: number) => {
    const reordered = [...images];
    const [moved] = reordered.splice(fromIndex, 1);
    reordered.splice(toIndex, 0, moved);
    onChange(reordered);
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {images.map((url, index) => (
          <div
            key={url}
            className="relative aspect-square bg-gray-100 rounded-lg overflow-hidden group"
            draggable
            onDragStart={(e) => e.dataTransfer.setData('index', String(index))}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              const fromIndex = parseInt(e.dataTransfer.getData('index'));
              handleReorder(fromIndex, index);
            }}
          >
            <Image src={url} alt="" fill className="object-cover" />
            <button
              onClick={() => handleRemove(index)}
              className="absolute top-2 right-2 w-6 h-6 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
            >
              ×
            </button>
            {index === 0 && (
              <span className="absolute bottom-2 left-2 text-xs bg-black/70 text-white px-2 py-1 rounded">
                Main
              </span>
            )}
          </div>
        ))}

        {images.length < maxImages && (
          <label className="aspect-square border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-gray-400 transition-colors">
            <input
              type="file"
              multiple
              accept="image/jpeg,image/png,image/webp"
              onChange={(e) => e.target.files && handleUpload(e.target.files)}
              className="hidden"
              disabled={uploading}
            />
            {uploading ? (
              <div className="animate-spin w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full" />
            ) : (
              <>
                <span className="text-2xl text-gray-400">+</span>
                <span className="text-xs text-gray-400 mt-1">Add images</span>
              </>
            )}
          </label>
        )}
      </div>

      <p className="text-xs text-gray-500">
        Drag images to reorder. First image is the main product image.
        {images.length}/{maxImages} images
      </p>
    </div>
  );
}
```

## Image Optimisation

### Next.js Image Configuration

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.supabase.co',
        pathname: '/storage/v1/object/public/**',
      },
    ],
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
};

export default config;
```

### Responsive Image Component

```typescript
// src/components/OptimisedImage.tsx
import Image from 'next/image';

interface OptimisedImageProps {
  src: string;
  alt: string;
  aspectRatio?: 'square' | 'video' | 'portrait' | 'wide';
  priority?: boolean;
  className?: string;
}

const aspectRatios = {
  square: 'aspect-square',
  video: 'aspect-video',
  portrait: 'aspect-[3/4]',
  wide: 'aspect-[21/9]',
};

export function OptimisedImage({
  src,
  alt,
  aspectRatio = 'square',
  priority = false,
  className = '',
}: OptimisedImageProps) {
  return (
    <div className={`relative overflow-hidden ${aspectRatios[aspectRatio]} ${className}`}>
      <Image
        src={src}
        alt={alt}
        fill
        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
        className="object-cover"
        priority={priority}
      />
    </div>
  );
}
```

## Storage Migration Script

```sql
-- Migration: 002_storage_buckets.sql

-- Create buckets
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES
  ('product-images', 'product-images', true, 5242880,
   ARRAY['image/jpeg', 'image/png', 'image/webp', 'image/avif']),
  ('cms-images', 'cms-images', true, 10485760,
   ARRAY['image/jpeg', 'image/png', 'image/webp', 'image/avif', 'image/svg+xml']),
  ('category-images', 'category-images', true, 5242880,
   ARRAY['image/jpeg', 'image/png', 'image/webp', 'image/avif']),
  ('order-attachments', 'order-attachments', false, 20971520, NULL)
ON CONFLICT (id) DO NOTHING;

-- Public bucket policies
CREATE POLICY "Public read access" ON storage.objects
FOR SELECT USING (bucket_id IN ('product-images', 'cms-images', 'category-images'));

CREATE POLICY "Admin upload access" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id IN ('product-images', 'cms-images', 'category-images')
  AND EXISTS (
    SELECT 1 FROM public.user_roles
    WHERE user_id = auth.uid()
    AND role_id IN ('super_admin', 'admin', 'shop_editor', 'cms_editor')
  )
);

CREATE POLICY "Admin update access" ON storage.objects
FOR UPDATE USING (
  bucket_id IN ('product-images', 'cms-images', 'category-images')
  AND EXISTS (
    SELECT 1 FROM public.user_roles
    WHERE user_id = auth.uid()
    AND role_id IN ('super_admin', 'admin', 'shop_editor', 'cms_editor')
  )
);

CREATE POLICY "Admin delete access" ON storage.objects
FOR DELETE USING (
  bucket_id IN ('product-images', 'cms-images', 'category-images')
  AND EXISTS (
    SELECT 1 FROM public.user_roles
    WHERE user_id = auth.uid()
    AND role_id IN ('super_admin', 'admin', 'shop_editor', 'cms_editor')
  )
);

-- Private bucket policies
CREATE POLICY "Users view own order attachments" ON storage.objects
FOR SELECT USING (
  bucket_id = 'order-attachments'
  AND (
    EXISTS (
      SELECT 1 FROM public.orders
      WHERE orders.id::text = (storage.foldername(name))[1]
      AND (orders.user_id = auth.uid() OR orders.customer_email = auth.jwt()->>'email')
    )
    OR EXISTS (
      SELECT 1 FROM public.user_roles
      WHERE user_id = auth.uid()
      AND role_id IN ('super_admin', 'admin', 'shop_editor')
    )
  )
);

CREATE POLICY "Admin upload order attachments" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'order-attachments'
  AND EXISTS (
    SELECT 1 FROM public.user_roles
    WHERE user_id = auth.uid()
    AND role_id IN ('super_admin', 'admin', 'shop_editor')
  )
);
```

## Checklist

```markdown
## Storage Setup Checklist

- [ ] Created product-images bucket (public, 5MB limit)
- [ ] Created cms-images bucket (public, 10MB limit)
- [ ] Created category-images bucket (public, 5MB limit)
- [ ] Created order-attachments bucket (private, 20MB limit)
- [ ] Applied public read policies
- [ ] Applied admin upload/update/delete policies
- [ ] Applied private bucket user access policies
- [ ] Configured Next.js image domains
- [ ] Created storage utility library
- [ ] Created ImageUpload component
- [ ] Created GalleryUpload component
- [ ] Tested upload from admin
- [ ] Tested public image display
- [ ] Verified RLS policies work correctly
```
