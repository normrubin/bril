function benchmark(iterations: bigint): bigint {
  let sum: bigint = 0n;
  let product: bigint = 1n;
  let flag: bigint = 1n; // Use 1n for true, 0n for false

  for (let i: bigint = 0n; i < iterations; i = i + 1n) {
    sum = sum + i;
    product = product * 2n;
    
    // Toggle flag between 0 and 1
    flag = 1n - flag;

    if (flag === 0n) {
      sum = sum - product;
    } else {
      sum = sum + product;
    }
  }

  return sum;
}

const result: bigint = benchmark(10n);
console.log(result);