interface ApiFetchOptions {
  method?: string;
  body?: any;
  headers?: Record<string,string>;
  isForm?: boolean;
}

export async function apiFetch(url: string, options?: ApiFetchOptions) {
  const {method='GET', body, headers={}, isForm=false} = options || {};
  const finalHeaders = isForm ? {} : {'Content-Type':'application/json', ...headers};

  const res = await fetch(`${process.env.REACT_APP_API_URL}${url}`, {
    method,
    body,
    headers: finalHeaders,
    credentials: 'include'
  });

  if (!res.ok) {
    let errMsg = "API Error";
    try {
      const errData = await res.json();
      errMsg = errData.error || errMsg;
    } catch {}
    throw new Error(errMsg);
  }

  return res.json().catch(()=> ({}));
}
