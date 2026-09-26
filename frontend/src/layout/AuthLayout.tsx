import { Outlet } from "react-router";
import { MeshGradientBackground } from "#components/ui/mesh-gradient";

const AuthLayout = () => {
  return (
    <div className="h-screen items-center justify-center flex bg-slate-950">
      <MeshGradientBackground />
      <div className="bg-white p-4 rounded-xl w-full max-w-md flex justify-center flex-col gap-4 z-50">
        <Outlet />
      </div>
    </div>
  );
};

export default AuthLayout;
