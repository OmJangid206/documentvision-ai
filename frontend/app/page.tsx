"use client";

import { useState } from "react";

interface ExtractedData {
    full_name: string | null;
    date_of_birth: string | null;
    address: string | null;
    id_number: string | null;
    document_type: string | null;
    confidence_score: number | null;

    success?: boolean;
    error?: string;
}

interface DocumentResult {
    file_name: string;
    extracted_data: ExtractedData;
}

interface ApiResponse {
    success: boolean;
    results: DocumentResult[];
}

// File: frontend/app/page.tsx

export default function HomePage() {
    const [files, setFiles] = useState<FileList | null>(null);
    const [results, setResults] = useState<DocumentResult[]>([]);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFiles(e.target.files);
    };

    const handleUpload = async () => {
        if (!files || files.length === 0) {
            alert("Please select at least one document.");
            return;
        }

        setLoading(true);

        const formData = new FormData();

        Array.from(files).forEach((file) => {
            formData.append("files", file);
        });

        try {
            const response = await fetch("http://127.0.0.1:8000/upload-documents", {
                method: "POST",
                body: formData,
            });

            const data: ApiResponse = await response.json();
            setResults(data.results || []);
        } catch (error) {
            console.error(error);
            alert("Failed to process documents.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-7xl mx-auto">
                <h1 className="text-3xl font-bold mb-2">DocumentVision AI</h1>
                <p className="text-gray-600 mb-8">
                    AI-Powered Document Data Extraction Dashboard
                </p>

                <div className="bg-white rounded-2xl shadow-sm border p-6 mb-8">
                    <h2 className="text-xl font-semibold mb-4">Upload Documents</h2>

                    <label className="border-2 border-dashed border-gray-300 rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer hover:border-black transition mb-6">

                        <div className="text-4xl mb-3">📄</div>

                        <p className="text-lg font-medium">
                            Click to upload documents
                        </p>

                        <p className="text-sm text-gray-500 mt-1">
                            PDF, JPG, PNG supported
                        </p>

                        {files && (
                            <p className="text-sm text-green-600 mt-3 font-medium">
                                {files.length} file(s) selected
                            </p>
                        )}

                        <input
                            type="file"
                            multiple
                            accept=".pdf,.png,.jpg,.jpeg"
                            onChange={handleFileChange}
                            className="hidden"
                        />
                    </label>

                    <button
                        onClick={handleUpload}
                        disabled={loading}
                        className="px-6 py-3 rounded-xl bg-black text-white font-medium disabled:opacity-50"
                    >
                        {loading ? "Processing..." : "Upload & Extract"}
                    </button>
                </div>

                {results.length > 0 && (
                    <div className="bg-white rounded-2xl shadow-sm border p-6 overflow-x-auto">
                        <h2 className="text-xl font-semibold mb-4">Extracted Results</h2>

                        <table className="w-full text-sm border-collapse">
                            <thead>
                                <tr className="border-b text-left">
                                    <th className="py-3 pr-4">File Name</th>
                                    <th className="py-3 pr-4">Document Type</th>
                                    <th className="py-3 pr-4">Full Name</th>
                                    <th className="py-3 pr-4">DOB</th>
                                    <th className="py-3 pr-4">ID Number</th>
                                    <th className="py-3 pr-4">Address</th>
                                    <th className="py-3 pr-4">Confidence</th>
                                </tr>
                            </thead>

                            <tbody>
                                {results.map((doc, index) => (
                                    <tr key={index} className="border-b align-top">
                                        <td className="py-4 pr-4">{doc.file_name}</td>

                                        {doc.extracted_data.error ? (
                                            <td colSpan={6} className="py-4 pr-4 text-red-600 font-medium">
                                                {doc.extracted_data.error}
                                            </td>
                                        ) : (
                                            <>
                                                <td className="py-4 pr-4">
                                                    {doc.extracted_data.document_type || "-"}
                                                </td>

                                                <td className="py-4 pr-4">
                                                    {doc.extracted_data.full_name || "-"}
                                                </td>

                                                <td className="py-4 pr-4">
                                                    {doc.extracted_data.date_of_birth || "-"}
                                                </td>

                                                <td className="py-4 pr-4">
                                                    {doc.extracted_data.id_number || "-"}
                                                </td>

                                                <td className="py-4 pr-4">
                                                    {doc.extracted_data.address || "-"}
                                                </td>

                                                <td className="py-4 pr-4">
                                                    {doc.extracted_data.confidence_score ?? "-"}
                                                </td>
                                            </>
                                        )}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </main>
    );
}
