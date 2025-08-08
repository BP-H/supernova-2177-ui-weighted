import dynamic from "next/dynamic";
const Universe3D = dynamic(() => import("@/components/Universe3D"), { ssr: false });

export default function UniversePage() {
  return (
    <div style={{height: "100vh", background:"#000"}}>
      <Universe3D />
    </div>
  );
}
