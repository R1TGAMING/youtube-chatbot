import { createClient, SupabaseClient } from "@supabase/supabase-js";

const supabase_url: string = import.meta.env.VITE_SUPABASE_URL;
const supabase_anon_key: string = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase: SupabaseClient = createClient(
  supabase_url,
  supabase_anon_key,
);
