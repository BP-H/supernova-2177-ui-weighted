import { redirect } from "next/navigation";

export default function Index() {
  redirect("/feed");
  return null;
}
