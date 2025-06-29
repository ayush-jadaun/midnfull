import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import LottieLoader from "../../components/LottieLoader";
import { router } from "expo-router";

export default function OnboardingStep1() {
  return (
    <View style={styles.container}>
      <LottieLoader source={require("../../assets/lottie/onboarding1.json")} />
      <Text style={styles.title}>Welcome to Mindful App!</Text>
      <Text style={styles.text}>
        We're glad you're here. Mindful App is your safe space for self-care and
        growth. Our mission: Help you nurture your mental well-being, one
        mindful moment at a time.
      </Text>
      <Button
        title="Next"
        color="#1976D2"
        onPress={() => router.push("/step2")}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#A7C7E7", // Soft blue
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#1976D2",
    marginBottom: 20,
  },
  text: {
    fontSize: 18,
    color: "#2D3A4A",
    textAlign: "center",
    marginBottom: 40,
  },
});
