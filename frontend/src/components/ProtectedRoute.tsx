import { useEffect } from "react";
import { supabase } from "../utils/supabase";
import { Outlet, useNavigate, type NavigateFunction } from "react-router";

const ProtectedRoute = () => {
  const navigate: NavigateFunction = useNavigate();

  useEffect(() => {
    const getSession = async (): Promise<void> => {
      const { data, error } = await supabase.auth.getSession();

      if (!data.session) {
        navigate("/login");
      }

      if (error) {
        console.error(error);
        navigate("/login");
      }
    };

    getSession();
  }, [navigate]);

  return <Outlet />;
};

export default ProtectedRoute;
