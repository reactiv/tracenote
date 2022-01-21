import * as React from "react";

export const fetcher = (...args) => fetch(...args).then(res => res.json())
