export function formatBalance(balance: number | null): string {
  if (balance === null) return "0.00";
  // Convert from lamports to SOL (1 SOL = 1e9 lamports)
  const solBalance = balance / 1e9;
  return solBalance.toFixed(2);
}
