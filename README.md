<h1>Fendimo</h1>
<a>
<image src='https://github.com/TherealArithmeticProgression/Fendimo-Version-Control-System-Inspired-by-Git/blob/main/image.png', alt='Fendimo Logo'>
</a>


<h2>How is Fendimo any different from Git?</h2>

<h3> It defaults to SHA-256</h3>
Git relies on SHA-1/SHA-1DC to maintain backward compatability, but researchers in the past have successfully demonstrated that SHA-1 can undergo [collision attacks](https://qodex.ai/blog/sha1-vs-sha256). Although Git is actively moving in the forward direction, Fendimo defaults to the SHA-2 (aka, SHA-256) algorithm (SHA-3 would be a better alternative, but SHA-256 is optimized for speed). 

<h2> Note </h2>
This underlying code was inspired by the code @ [the ugit guide](https://www.leshenko.net/p/ugit/). Create a pullrequest for any suggested changes. Thanks!