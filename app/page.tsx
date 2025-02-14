"use client";

import { useState } from "react";
import { CarIcon } from "lucide-react";

export default function Home() {
  const [image, setImage] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [formData, setFormData] = useState({
    damageType: '',
    carMake: '',
    carModel: '',
    year: '',
    mileage: ''
  });

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          setImage(e.target?.result as string);
        };
        reader.readAsDataURL(file);

        // Send image to backend
        const formData = new FormData();
        formData.append('image', file);
        
        try {
          const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
          });
          
          if (!response.ok) {
            throw new Error('Upload failed');
          }
          
          const data = await response.json();
          console.log('Upload successful:', data);
        } catch (error) {
          console.error('Error uploading image:', error);
        }
      }
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleGeneratePrice = () => {
    console.log('Generating price with:', { image, ...formData });
  };

  return (
    <main className="min-h-screen bg-[#121212] relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-900/30 rounded-full blur-3xl pointer-events-none" />
      
      <div className="relative max-w-6xl mx-auto px-4 py-12">
        <div className="flex items-center justify-center mb-12">
          <CarIcon className="w-8 h-8 text-purple-500 mr-2" />
          <h1 className="text-4xl font-bold text-white">Biddify</h1>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          {/* Drag & Drop Section */}
          <div
            className={`
              relative rounded-lg border-2 border-dashed p-8 transition-colors bg-gray-800/30
              ${dragActive ? 'border-purple-500 bg-purple-500/10' : 'border-gray-700 hover:border-purple-500/50'}
              ${image ? 'bg-gray-800/50' : ''}
            `}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {image ? (
              <img
                src={image}
                alt="Uploaded vehicle"
                className="w-full h-[300px] object-cover rounded-md"
              />
            ) : (
              <div className="h-[300px] flex flex-col items-center justify-center text-gray-400">
                <svg
                  className="w-12 h-12 mb-4 text-gray-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
                <p className="text-lg">Drag and drop your vehicle image here</p>
                <p className="text-sm text-gray-500 mt-2">Supports: JPG, PNG, GIF</p>
              </div>
            )}
          </div>

          {/* Form Section */}
          <div className="bg-gray-800/30 p-8 rounded-lg space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-200">Damage Type</label>
              <input
                type="text"
                name="damageType"
                value={formData.damageType}
                onChange={handleInputChange}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                placeholder="Enter damage type"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-200">Car Make</label>
              <input
                type="text"
                name="carMake"
                value={formData.carMake}
                onChange={handleInputChange}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                placeholder="Enter car make"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-200">Car Model</label>
              <input
                type="text"
                name="carModel"
                value={formData.carModel}
                onChange={handleInputChange}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                placeholder="Enter car model"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-200">Year</label>
              <input
                type="text"
                name="year"
                value={formData.year}
                onChange={handleInputChange}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                placeholder="Enter year"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-200">Mileage</label>
              <input
                type="text"
                name="mileage"
                value={formData.mileage}
                onChange={handleInputChange}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                placeholder="Enter mileage"
              />
            </div>
          </div>
        </div>

        {/* Centered Generate Price Button */}
        <div className="flex justify-center">
          <button
            onClick={handleGeneratePrice}
            className="px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors text-lg font-semibold"
          >
            Generate Price
          </button>
        </div>
      </div>
    </main>
  );
}