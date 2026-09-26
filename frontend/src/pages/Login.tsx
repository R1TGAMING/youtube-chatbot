import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router";
import { supabase } from "../utils/supabase";

const Login = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>();
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const checkSession = async () => {
      const { data, error } = await supabase.auth.getSession();

      if (data.session) {
        navigate("/dashboard");
      }

      if (error) {
        console.error(error);
      }
    };

    checkSession();
  }, [navigate]);

  const handleSubmit = async (
    e: React.SubmitEvent<HTMLFormElement>,
  ): Promise<void> => {
    e.preventDefault();
    setLoading(true);

    const { data, error } = await supabase.auth.signInWithPassword({
      email: email,
      password: password,
    });

    if (error) {
      setLoading(false);

      if (error.code === "invalid_credentials") {
        setError("Invalid Credentials");
      } else {
        setError("Error has encured please try again..");
      }

      console.error(error);
    }

    if (data.session) {
      setLoading(false);
      navigate("/dashboard");
    }
  };

  return (
    <>
      <div>
        <h2 className="text-4xl tracking-wide font-bold">Login</h2>
        <p className="text-slate-400">Log in to your account</p>
      </div>

      <form className="flex flex-col gap-2" onSubmit={handleSubmit}>
        <label>Email</label>
        <input
          type="email"
          id="email"
          name="email"
          placeholder="Input here..."
          className="border-b-2 focus:outline-none rounded "
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <label className="mt-4">Password</label>
        <input
          type="password"
          id="username"
          name="username"
          placeholder="Your password"
          className="border-b-2 focus:outline-none rounded focus:border-b-gray-100"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <p className="mt-4">
          Doesn`t have an account?
          <Link
            className="text-blue-400 underline cursor-pointer hover:text-blue-600"
            to={"/register"}
          >
            &nbsp;Click here
          </Link>
        </p>
        <button
          type="submit"
          className="bg-gray-950 rounded-xl  hover:bg-gray-800 text-white font-black p-4 cursor-pointer transition-all duration-300 ease-in-out"
        >
          {loading ? <>Loading...</> : <>Login</>}
        </button>
        {error ? <p className="text-red-400">{error}</p> : <></>}
      </form>
    </>
  );
};

export default Login;
