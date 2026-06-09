export async function runIngest(id) {
  const runIngest = async () => {
  await fetch(
    "http://localhost:8000/api/ingesta",
    {
      method: "POST"
    }
  );

  refetch();
};

  return await response.json();
}

