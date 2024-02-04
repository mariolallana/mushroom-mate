import * as React from "react";
import beneficio1 from '../assets/beneficio1.png';
import beneficio2 from '../assets/beneficio2.png';
import beneficio3 from '../assets/beneficio3.png';

function HomePageThree() {
  return (
    <div className="flex flex-col justify-center items-center px-5 py-12 bg-green-800 bg-opacity-60">
      <div className="flex flex-col items-stretch mt-4 w-full max-w-full">
        <header className="self-center text-4xl font-bold text-center text-white max-md:max-w-full">
          Discover the Magic of Mushroom Foraging
        </header>
        <div className="mt-8 max-md:max-w-full">
          <div className="flex gap-5 max-md:flex-col max-md:gap-0 max-md:items-stretch">
            <div className="flex flex-col items-stretch w-[34%] max-md:ml-0 max-md:w-full">
              <div className="flex flex-col grow items-center mt-2.5 text-center text-white max-md:mt-10">
                <img
                  loading="lazy"
                  srcSet={beneficio1} className="object-center w-32 max-w-full aspect-[1.06]"
                  alt="Explore Breathtaking Forests"
                />
                <div className="mt-9 text-2xl font-bold">Explore Breathtaking Forests</div>
                <div className="self-stretch mt-7 text-lg">
                  Immerse yourself in the beauty of nature as you traverse through lush green forests
                </div>
              </div>
            </div>
            <div className="flex flex-col items-stretch ml-5 w-[38%] max-md:ml-0 max-md:w-full">
              <div className="flex flex-col items-center text-center text-white max-md:mt-10">
                <img
                  loading="lazy"
                  srcSet={beneficio2} className="object-center aspect-[0.61] w-[85px]"
                  alt="Find Exquisite Mushrooms"
                />
                <div className="mt-7 text-2xl font-bold">Find Exquisite Mushrooms</div>
                <div className="self-stretch mt-7 text-lg">
                  Discover a variety of mushrooms, from the common to the rare and exotic
                </div>
              </div>
            </div>
            <div className="flex flex-col items-stretch ml-5 w-[28%] max-md:ml-0 max-md:w-full">
              <div className="flex flex-col items-stretch text-center text-white max-md:mt-10">
                <img
                  loading="lazy"
                  srcSet={beneficio3} className="object-center self-center max-w-full aspect-square w-[157px]"
                  alt="Conquer Majestic Mountains"
                />
                <div className="mt-2 text-2xl font-bold">Conquer Majestic Mountains</div>
                <div className="mt-6 text-lg">Embark on a thrilling uphill journey to uncover hidden mushroom treasures</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePageThree;
