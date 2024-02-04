import * as React from "react";

function Footer() {
  return (
    <div className="flex flex-col justify-center items-center px-5 py-12 bg-green-800 bg-opacity-60">
      <div className="flex flex-col items-stretch mt-4 w-full max-w-full">
        <header className="self-center text-4xl font-bold text-center text-white max-md:max-w-full">
        Join the Mushroom Foraging Community
        </header>
        <div className="mt-8 max-md:max-w-full">
          <div className="flex gap-5 max-md:flex-col max-md:gap-0 max-md:items-stretch">
            <div className="flex flex-col items-stretch w-[34%] max-md:ml-0 max-md:w-full">
              <div className="flex flex-col grow items-center mt-2.5 text-center text-white max-md:mt-10">
                <div className="mt-9 text-2xl font-bold">Connect with Like-minded Enthusiasts</div>
                <div className="self-stretch mt-7 text-lg">
                Share your experiences, tips, and findings with a community of passionate mushroom foragers
                </div>
              </div>
            </div>
            <div className="flex flex-col items-stretch ml-5 w-[38%] max-md:ml-0 max-md:w-full">
              <div className="flex flex-col items-center text-center text-white max-md:mt-10">
                <div className="mt-7 text-2xl font-bold">Discover Expert Expertise</div>
                <div className="self-stretch mt-7 text-lg">
                Learn from experienced foragers and gain valuable insights into mushroom foraging techniques
                </div>
              </div>
            </div>
            <div className="flex flex-col items-stretch ml-5 w-[28%] max-md:ml-0 max-md:w-full">
              <div className="flex flex-col items-stretch text-center text-white max-md:mt-10">
                <div className="mt-2 text-2xl font-bold">Conquer Majestic Mountains</div>
                <div className="mt-6 text-lg">Get the latest news and updates on mushroom foraging events, workshops, and gatherings</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Footer;
