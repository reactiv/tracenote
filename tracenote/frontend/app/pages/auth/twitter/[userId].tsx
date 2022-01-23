import React, {useState, useEffect} from "react";
import { useRouter } from "next/router";

const TwitterAuth = () => {
  const router = useRouter();
  console.log(router.query);
  return (
    <div>
      <h1>Twitter Auth: {router.query.oauth_token}</h1>
    </div>
  );
}

export default TwitterAuth;