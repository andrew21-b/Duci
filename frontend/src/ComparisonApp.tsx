
import { useState } from "react";
import { Button } from "./components/ui/button";
import { Slider } from "./components/ui/slider";

export default function ComparisonApp() {
  const [before, setBefore] = useState<File | null>(null);
  const [after, setAfter] = useState<File | null>(null);
  const [diff, setDiff] = useState<string | null>(null);
  const [score, setScore] = useState<string | null>(null);
  const [threshold, setThreshold] = useState<number>(30);
  const [loading, setLoading] = useState<boolean>(false);

  const handleUpload = async () => {
    if (!before || !after) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("before", before);
    formData.append("after", after);
    formData.append("threshold", threshold.toString());

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/comparison/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setScore(Number(data.difference_score).toFixed(2));
      setDiff(`http://localhost:8000${data.diff_image_url}`);
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Visual Change Detection MVP</h1>


      <div className="grid grid-cols-2 gap-4">
        <label className="flex flex-col items-center justify-center border-2 border-dashed rounded-lg h-40 cursor-pointer bg-white hover:bg-gray-100 transition">
          {before ? (
            <img src={URL.createObjectURL(before)} alt="Before Preview" className="h-36 object-contain" />
          ) : (
            <span className="text-gray-400">Click to upload Before image</span>
          )}
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={e => setBefore(e.target.files ? e.target.files[0] : null)}
          />
        </label>

        <label className="flex flex-col items-center justify-center border-2 border-dashed rounded-lg h-40 cursor-pointer bg-white hover:bg-gray-100 transition">
          {after ? (
            <img src={URL.createObjectURL(after)} alt="After Preview" className="h-36 object-contain" />
          ) : (
            <span className="text-gray-400">Click to upload After image</span>
          )}
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={e => setAfter(e.target.files ? e.target.files[0] : null)}
          />
        </label>
      </div>


      <div>
        <label className="block text-sm mb-2">Sensitivity Threshold: {threshold}</label>
        <Slider
          defaultValue={[threshold]}
          max={100}
          step={1}
          onValueChange={(val: number[]) => setThreshold(val[0])}
        />
      </div>

      <Button onClick={handleUpload} disabled={loading || !before || !after}>
        {loading ? "Comparing..." : "Compare"}
      </Button>


      {score && before && after && (
        <div className="space-y-4">
          <p className="text-lg font-medium">Difference Score: <span className="font-bold">{score}%</span></p>

          <div className="flex flex-row justify-center items-start gap-8">
            <div className="flex flex-col items-center">
              <h3 className="text-sm font-semibold mb-1">Before</h3>
              <img src={URL.createObjectURL(before)} alt="Before" className="rounded shadow" />
            </div>
            <div className="flex flex-col items-center">
              <h3 className="text-sm font-semibold mb-1">After</h3>
              <img src={URL.createObjectURL(after)} alt="After" className="rounded shadow" />
            </div>
            <div className="flex flex-col items-center">
              <h3 className="text-sm font-semibold mb-1">Diff</h3>
              {diff && <img src={diff} alt="Diff" className="rounded shadow" />}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
